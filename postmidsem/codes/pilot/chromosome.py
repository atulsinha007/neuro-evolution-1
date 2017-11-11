# chromosome.py

import gene
import matenc
import numpy as np
import tensorflow as tf
import deep_net
import time

innov_ctr = None




class Chromosome:
    """
    def __init__(self,dob,node_arr=[],conn_arr=[],bias_arr=[]):
        self.node_arr = node_arr	#list of node objects
        self.conn_arr = conn_arr	#list of conn objects
        self.bias_conn_arr = bias_arr	#list of BiasNode objects
        self.dob = dob 				#the generation in which it was created.
        self.node_ctr=len(node_arr)+1
    """
        #here initialization is always with simplest chromosome (AND mainly for innov ctr) , here could be an error
    def __init__(self,inputdim,outputdim):
        global innov_ctr

        self.node_ctr = inputdim + outputdim + 1
        innov_ctr = 1  # Warning!! these two lines change(reset) global variables, here might be some error
        lisI = [gene.Node(num_setter, 'I') for num_setter in range(1, self.node_ctr - outputdim)]
        lisO = [gene.Node(num_setter, 'O') for num_setter in range(inputdim + 1, self.node_ctr)]
        self.node_arr = lisI + lisO
        self.conn_arr=[]
        for inputt in lisI:
            for outputt in lisO:
                self.conn_arr.append(gene.Conn(innov_ctr, (inputt, outputt), np.random.random(), status=True))

                innov_ctr += 1
        self.bias_conn_arr = []
        self.bias_conn_arr = [gene.BiasConn(outputt, np.random.random()/1000) for outputt in lisO]
        self.dob = 0

    def reset_chromo_to_zero(self):
        self.node_ctr = 0
        self.node_arr = []
        self.conn_arr = []
        self.bias_conn_arr = []

    def set_node_ctr(self, ctr=None):
        if not ctr:
            ctr = len(self.node_arr) + 1
        self.node_ctr = ctr

    def pp(self):
        print("\nNode List")
        [item.pp() for item in self.node_arr]

        print("\n\nConnection List")
        [item.pp() for item in self.conn_arr]

        print("\n\nBias Connection List")
        [item.pp() for item in self.bias_conn_arr]
        print("dob", self.dob, "node counter", self.node_ctr)
        print("--------------------------------------------")

    def convert_to_MatEnc(self, inputdim, outputdim):

        ConnMatrix = {}  # Connection Matrix
        WeightMatrix = {}  # Weight Matrix
        NatureCtrDict = {}  # Contains Counter of Nature { 'I', 'H1', 'H2', 'O' }
        NatureCtrDict['I'] = 0
        NatureCtrDict['H1'] = 0
        NatureCtrDict['H2'] = 0
        NatureCtrDict['O'] = 0

        dictionary = {}  # Contains node numbers mapping starting from 0, nature-wise
        dictionary['I'] = {}
        dictionary['H1'] = {}
        dictionary['H2'] = {}
        dictionary['O'] = {}
        couple_to_conn_map = {}

        for i in self.node_arr:
            dictionary[i.nature][i] = NatureCtrDict[i.nature]
            NatureCtrDict[i.nature] += 1

        ConnMatrix['IO'] = np.zeros((inputdim, outputdim))
        ConnMatrix['IH1'] = np.zeros((inputdim, NatureCtrDict['H1']))
        ConnMatrix['IH2'] = np.zeros((inputdim, NatureCtrDict['H2']))
        ConnMatrix['H1H2'] = np.zeros((NatureCtrDict['H1'], NatureCtrDict['H2']))
        ConnMatrix['H1O'] = np.zeros((NatureCtrDict['H1'], outputdim))
        ConnMatrix['H2O'] = np.zeros((NatureCtrDict['H2'], outputdim))

        WeightMatrix['IO'] = np.zeros((inputdim, outputdim))
        WeightMatrix['IH1'] = np.zeros((inputdim, NatureCtrDict['H1']))
        WeightMatrix['IH2'] = np.zeros((inputdim, NatureCtrDict['H2']))
        WeightMatrix['H1H2'] = np.zeros((NatureCtrDict['H1'], NatureCtrDict['H2']))
        WeightMatrix['H1O'] = np.zeros((NatureCtrDict['H1'], outputdim))
        WeightMatrix['H2O'] = np.zeros((NatureCtrDict['H2'], outputdim))

        for con in self.conn_arr:
            if con.status == True:
                ConnMatrix[con.source.nature + con.destination.nature][
                    dictionary[con.source.nature][con.source]][
                    dictionary[con.destination.nature][con.destination]] = 1
            couple_to_conn_map[con.get_couple()] = con
            WeightMatrix[con.source.nature + con.destination.nature][dictionary[con.source.nature][con.source]][
                dictionary[con.destination.nature][con.destination]] = con.weight

        inv_dic = {key: {v: k for k, v in dictionary[key].items()} for key in dictionary.keys()}

        new_encoding = matenc.MatEnc(WeightMatrix, ConnMatrix, self.bias_conn_arr, inv_dic, couple_to_conn_map,
                                     self.node_arr,self.conn_arr)

        return new_encoding

    def modify_thru_backprop(self, inputdim, outputdim, trainx, trainy, epochs=10, learning_rate=0.1, n_par=10):

        x = tf.placeholder(shape=[None, inputdim], dtype=tf.float32)
        y = tf.placeholder(shape=[None, ], dtype=tf.int32)
        n_par = n_par
        par_size = tf.shape(trainx)[0] // n_par
        prmsdind = tf.placeholder(name='prmsdind', dtype=tf.int32)
        valid_x_to_be = trainx[prmsdind * par_size:(prmsdind + 1) * par_size, :]
        valid_y_to_be = trainy[prmsdind * par_size:(prmsdind + 1) * par_size]
        train_x_to_be = tf.concat(
            (trainx[:(prmsdind) * par_size, :], trainx[(prmsdind + 1) * par_size:, :]),
            axis=0)
        train_y_to_be = tf.concat(
            (trainy[:(prmsdind) * par_size], trainy[(prmsdind + 1) * par_size:]), axis=0)

        mat_enc = self.convert_to_MatEnc(inputdim, outputdim)
        newneu_net = deep_net.DeepNet(x, inputdim, outputdim, mat_enc)

        cost = newneu_net.negative_log_likelihood(y)
        print(newneu_net.mat_enc.CMatrix['IO'])
        optmzr = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost, var_list=newneu_net.params)
        # savo1 = tf.train.Saver(var_list=[self.srest_setx, self.srest_sety, self.stest_setx, self.stest_sety])
        with tf.Session() as sess:

            sess.run(tf.global_variables_initializer())

            # err = sess.run(newneu_net.errors(y), feed_dict={x: trainx, y: trainy})
            # print("train error ", err)



            # just any no. which does not satisfy below condition

            prev = 7
            current = 5
            start1 = time.time()
            for epoch in range(epochs):
                listisi = []
                for ind in range(n_par):
                    _, bost = sess.run([optmzr, cost],
                                       feed_dict={x: train_x_to_be.eval(feed_dict={prmsdind: ind}),
                                                  y: train_y_to_be.eval(feed_dict={prmsdind: ind})})

                    if epoch % (epochs // 4) == 0:
                        q = newneu_net.errors(y).eval(
                            feed_dict={x: valid_x_to_be.eval(feed_dict={prmsdind: ind}),
                                       y: valid_y_to_be.eval(feed_dict={prmsdind: ind})})
                        listisi.append(q)
                if epoch % (epochs // 4) == 0:
                    prev = current
                    current = np.mean(listisi)
                    print('validation', current)
                    print(tf.reduce_sum(newneu_net.wei_mat_var_map['IO']).eval())

                if prev - current < 0.002:
                    break;
            end1 = time.time()
            print("time ", end1 - start1)

            for key in newneu_net.wei_mat_var_map.keys():
                newneu_net.mat_enc.WMatrix[key] = newneu_net.wei_mat_var_map[key].eval()
            for i in range(len(newneu_net.bias_wei_arr)):
                ar = newneu_net.bias_var.eval()
                newneu_net.mat_enc.Bias_conn_arr[i].set_weight(ar[i])
        print(newneu_net.mat_enc.CMatrix['IO'],'final')
        newchromo = newneu_net.mat_enc.convert_to_chromosome(inputdim,outputdim,self.dob)

        self.conn_arr = newchromo.conn_arr
        self.node_arr = newchromo.node_arr
        self.bias_conn_arr = newchromo.bias_conn_arr  # list of BiasNode objects
        self.dob = newchromo.dob  # the generation in which it was created.
        self.node_ctr = len(self.node_arr) + 1

        return newchromo

    def weight_mutation(self, rng,factor = 0.1):

        chosen_ind = rng.choice(range(len(self.conn_arr)))
        self.conn_arr[chosen_ind].weight += (rng.random() - 0.5)*2*factor
        return chosen_ind

    def edge_mutation(self,inputdim,outputdim,rng,list_of_structural_mutation_so_far):

        newmatenc = self.convert_to_MatEnc(inputdim, outputdim)
        key_list = list(newmatenc.WMatrix.keys())
        #key_list.remove('IO')
        print(key_list)

        chosen_key = rng.choice(key_list)

        mat = newmatenc.CMatrix[chosen_key]
        #print(chosen_key, mat.shape, list(newmatenc.node_map.items()))
        i = rng.randint(0,mat.shape[0])
        j = rng.randint(0,mat.shape[1])
        split_key1,split_key2 = matenc.split_key(chosen_key)
        print(split_key1, split_key2)
        couple = (newmatenc.node_map[split_key1][i], newmatenc.node_map[split_key2][j])
        ctr = 0
        while mat[i][j] != 0:
            i = rng.randint(0, mat.shape[0])
            j = rng.randint(0, mat.shape[1])
            if ctr>10:
                return
                break
            ctr += 1
        couple = (newmatenc.node_map[split_key1][i], newmatenc.node_map[split_key2][j])
        mat[i][j] = 1
        if not newmatenc.WMatrix[ chosen_key][i][j]:
            global innov_ctr
            con_obj = gene.Conn(innov_ctr, couple, (rng.random()-0.5)*2, True)
            innov_ctr += 1
            self.conn_arr.append(con_obj)
            normalize_conn_arr_for_this_gen(list_of_structural_mutation_so_far,con_obj )
            #con_obj.pp()
        else:

            con_obj = newmatenc.couple_to_conn_map[couple]
            con_obj.status = True

    def node_mutation(self,inputdim, outputdim, rng, list_of_structural_mutation_so_far):
        #global innov_ctr
        type = 0
        newmatenc = self.convert_to_MatEnc(inputdim,outputdim)
        key_list = ['IH2', 'H1O', 'IO']
        stlis = ['H1', 'H2', 'H2']
        #prob_list = [0.1, 0.3, 0.6]
        prndm = rng.random()
        if prndm >0.4:
            ind = 2
        elif prndm >0.1:
            ind = 1
        elif prndm >0:
            ind = 0
        chosen_key = key_list[ind]
        #key_list.remove('IO')
        #print(key_list)

        #chosen_key = (key_list)

        mat = newmatenc.CMatrix[chosen_key]
        #print(chosen_key, mat.shape, list(newmatenc.node_map.items()))
        i = rng.randint(0, mat.shape[0])
        j = rng.randint(0, mat.shape[1])
        split_key1, split_key2 = matenc.split_key(chosen_key)
        print(split_key1, split_key2)
        ctr = 0

        if not newmatenc.WMatrix[ chosen_key][i][j] and not type:
            while mat[i][j] == 0:
                i = rng.randint(0, mat.shape[0])
                j = rng.randint(0, mat.shape[1])
                if ctr > 10:
                    return

                ctr += 1
        couple = (newmatenc.node_map[split_key1][i], newmatenc.node_map[split_key2][j])
        global innov_ctr
        con_obj = newmatenc.couple_to_conn_map[couple]
        con_obj.status = False

        newnode = gene.Node(self.node_ctr, stlis[ind])
        self.node_ctr += 1
        new_conn1 = gene.Conn(innov_ctr, (con_obj.source, newnode), 1.0 , True)
        innov_ctr += 1
        new_conn2 = gene.Conn(innov_ctr, (newnode, con_obj.destination), con_obj.weight , True)
        innov_ctr += 1
        new_conn1.pp()
        new_conn2.pp()
        con_obj.pp()
        self.node_arr.append( newnode )
        self.conn_arr.append( new_conn1 )
        self.conn_arr.append( new_conn2 )

        normalize_conn_arr_for_this_gen(list_of_structural_mutation_so_far,con_obj )

    def do_mutation(self,rate_conn_weight, rate_conn_itself, rate_node, inputdim, outputdim, rng, list_of_sm_sofar):
        prnd = rng.random()
        if prnd < rate_conn_weight:
            self.weight_mutation(rng)
        prnd = rng.random()
        if prnd < rate_conn_itself:
            self.edge_mutation(inputdim, outputdim, rng, list_of_sm_sofar)
        prnd = rng.random()
        if prnd < rate_node:
            self.node_mutation(inputdim, outputdim, rng, list_of_sm_sofar)







# def rand_init(inputdim, outputdim):
#     global innov_ctr
#     newchromo = Chromosome(0)
#
#     newchromo.node_ctr = inputdim + outputdim + 1
#     innov_ctr = 1  # Warning!! these two lines change(reset) global variables, here might be some error
#     lisI = [gene.Node(num_setter, 'I') for num_setter in range(1, newchromo.node_ctr - outputdim)]
#     lisO = [gene.Node(num_setter, 'O') for num_setter in range(inputdim + 1, newchromo.node_ctr)]
#     newchromo.node_arr = lisI + lisO
#     for inputt in lisI:
#         for outputt in lisO:
#             newchromo.conn_arr.append(gene.Conn(innov_ctr, (inputt, outputt), np.random.random(), status=True))
#             innov_ctr += 1
#     newchromo.bias_arr = [gene.BiasConn(outputt, np.random.random()) for outputt in lisO]
#     newchromo.dob = 0
#     return newchromo
