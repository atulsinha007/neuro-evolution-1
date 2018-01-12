import os
import pandas as pd
import random
import numpy as np
import pickle
rng = random
#to convert .xlsx to feature array for source
'''source_data = pd.read_excel("./dataset_1/source_features.xlsx", header=None)
source_feat_mat = source_data.as_matrix() 
assert( source_feat_mat.shape[0] == 200 )
#to read the labels for source
file_ob = open( "./dataset_1/source_output.csv", "rb")
lis = file_ob.readlines()
lis = lis[1:]
assert( len(lis) == 200)
source_label_lis = [item.rstrip().lower().decode("utf-8") for item in lis]
ann = len(lis)
file_ob.close()

#converting label in string to that to corresponding number
sorted_lis = list(set( source_label_lis ))
sorted_lis.sort()
dic = { sorted_lis[i]:i for i in range(len(sorted_lis)) }
print(dic)
source_label_lis_num = [ dic[item] for item in source_label_lis ]'''
pstri = './'
path = 'pickle_jar/'

assert( os.path.isfile(os.path.join(pstri + path, 'src_data.pickle')))
fs = open( pstri + "pickle_jar/src_data.pickle", "rb")
source_feat_mat, source_label_lis_num_arr = pickle.load(fs)
fs.close()

dum_arr = source_label_lis_num_arr.reshape((source_label_lis_num_arr.shape[0], 1))
clumped_arr = np.concatenate( (source_feat_mat, dum_arr), axis = 1)
numlis = np.arange(clumped_arr.shape[0])
ann = source_feat_mat.shape[0]

rng.shuffle(numlis)
clumped_arr = clumped_arr[ numlis ]
clumped_source = clumped_arr[:]
print(clumped_arr[:3])
assert( os.path.isfile(os.path.join(pstri + path, 'tar_data.pickle')))
fs = open( pstri + "pickle_jar/tar_data.pickle", "rb")
target_feat_mat, target_label_lis_num_arr = pickle.load(fs)
bann = target_feat_mat.shape[0]
fs.close()

dum_arr = target_label_lis_num_arr.reshape((target_label_lis_num_arr.shape[0], 1))
clumped_arr = np.concatenate( (target_feat_mat, dum_arr), axis = 1)
#print(dic)
numlis = np.arange(clumped_arr.shape[0])
rng.shuffle(numlis)
clumped_arr = clumped_arr[ numlis ]
#clumped_arr = clumped_arr[ numlis ]
clumped_target = clumped_arr[:]

#rng.shuffle(pimadata)

def give_source_data(): 
	'''
		returns two tuples each tuple has one array as feature set and other as column arrray of numerical labels
		this one is for source
	'''
	aann = ann
	#print(aann)
	rest_setx=clumped_source[:aann,:-1]#tuple of two shared variable of array

	rest_sety=clumped_source[:aann,-1:]
	test_setx=clumped_source[aann:,:-1]
	test_sety=clumped_source[aann:,-1:]
	'''assert( rest_setx.shape == (150,128))
	#print(rest_sety.shape)
	assert( rest_sety.shape == (150,1))
	assert( test_setx.shape == (50,640))
	assert( test_sety.shape == (50,1))'''
	return ((rest_setx,rest_sety),(test_setx,test_sety))


def give_target_data():  
	bbann = (bann*3)//4
	rest_setx=clumped_target[:bbann,:-1]
	rest_sety=clumped_target[:bbann,-1:]
	test_setx=clumped_target[bbann:,:-1]
	test_sety=clumped_target[bbann:,-1:]
	#print(test_setx.shape)
	#print(test_sety.shape)
	'''assert( rest_setx.shape == (37,640))
	assert( rest_sety.shape == (37,1))
	assert( test_setx.shape == (13,640))
	assert( test_sety.shape == (13,1))'''
	return ((rest_setx,rest_sety),(test_setx,test_sety))

def give_source_data_just_src():
	'''
		returns two tuples each tuple has one array as feature set and other as column arrray of numerical labels
		this one is for source
	'''
	aann = ann*3//4
	#print(aann)
	rest_setx=clumped_source[:aann,:-1]#tuple of two shared variable of array

	rest_sety=clumped_source[:aann,-1:]
	test_setx=clumped_source[aann:,:-1]
	test_sety=clumped_source[aann:,-1:]
	'''assert( rest_setx.shape == (150,128))
	#print(rest_sety.shape)
	assert( rest_sety.shape == (150,1))
	assert( test_setx.shape == (50,640))
	assert( test_sety.shape == (50,1))'''
	return ((rest_setx,rest_sety),(test_setx,test_sety))
def give_target_data_just_src_just_tar():
	bbann = 0
	rest_setx=clumped_target[:bbann,:-1]
	rest_sety=clumped_target[:bbann,-1:]
	test_setx=clumped_target[bbann:,:-1]
	test_sety=clumped_target[bbann:,-1:]
	#print(test_setx.shape)
	#print(test_sety.shape)
	'''assert( rest_setx.shape == (37,640))
	assert( rest_sety.shape == (37,1))
	assert( test_setx.shape == (13,640))
	assert( test_sety.shape == (13,1))'''
	return ((rest_setx,rest_sety),(test_setx,test_sety))

def find_indices_dslr( target_label_lis_num_arr ):
	lis_of_number = [0]
	lis_of_cardinal = []

	#global lis_of_number, lis_of_cardinal

	prev_item = target_label_lis_num_arr[0]
	ctr = 0
	for i in range( target_label_lis_num_arr.shape[0]):
		if ( prev_item != target_label_lis_num_arr[i]):
			lis_of_cardinal += [ctr]
			ctr = 0
			prev_item = target_label_lis_num_arr[i]
		ctr += 1
	lis_of_cardinal += [ctr]
	lis_of_number = [lis_of_number[-1]+lis_of_cardinal[i] for i in range(len(lis_of_cardinal)) ]
	return lis_of_number, lis_of_cardinal
def give_rest_and_test( tup, indlow, indhigh):
	arr = tup[0][indlow:indhigh]
	label_arr = tup[1][ indlow: indhigh]
	pind = arr.shape[0]*3//4
	rest_arr = arr[:pind, :]
	rest_label = label_arr[:pind]
	test_arr = arr[pind:, :]
	test_label = label_arr[pind:]
	return (rest_arr, rest_label), (test_arr, test_label)
def make_test_ar_dslr(  tar_tup ):

	lis_of_number, lis_of_cardinal = find_indices_dslr( tar_tup )
	#tar_arr = tar_tup[0]
	#label_arr = tar_tup[1]
	#lis_to_return = []
	two_tup_lis = []
	tar_rest_arr_to_return = []
	tar_rest_label_to_return = []
	test_arr = []
	test_label = []
	for i in range(len(lis_of_number)-1):
		two_tup = give_rest_and_test( tar_tup, lis_of_number[i], lis_of_number[i+1])
		tar_rest_arr_to_return += two_tup[0][0].tolist()
		tar_rest_label_to_return += two_tup[0][1].tolist()
		test_arr += two_tup[1][0].tolist()
		test_label += two_tup[1][1].tolist()
	tar_rest_arr_to_return = np.array( tar_rest_arr_to_return, dtype = "float64")
	tar_rest_label_to_return = np.array( tar_rest_label_to_return, dtype = "float64")
	ran_lis = [i for i in range(tar_rest_arr_to_return.shape[0])]
	random.shuffle(ran_lis)
	tar_rest_arr_to_return = tar_rest_arr_to_return[ran_lis]
	tar_rest_label_to_return = tar_rest_label_to_return[ ran_lis ]

	test_arr = np.array( test_arr, dtype = "float64")
	test_label = np.array( test_label, dtype = "float64")
	test_lis_of_number, test_lis_of_cardinal = find_indices_dslr( (test_arr, test_label))
	for i in range( len(test_lis_of_number) - 1):
		major_arr = test_arr[ test_lis_of_number[i]: test_lis_of_number[i+1], :]
		major_label = test_label[test_lis_of_number[i]: test_lis_of_number[i+1]]
		minor_arr = np.concatenate((test_arr[:test_lis_of_number[i], :], test_arr[test_lis_of_number[i+1]:, :]))
		minor_label =  np.concatenate((test_label[:test_lis_of_number[i]], test_label[test_lis_of_number[i+1]:]))
		ran_lis = [i for i in range(minor_arr.shape[0])]
		sample_index_lis = random.sample(ran_lis, major_arr.shape[0])
		minor_arr = minor_arr[ sample_index_lis ]
		minor_label = minor_label[ sample_index_lis ]
		final_arr = np.concatenate( (major_arr, minor_arr))
		final_label = np.concatenate(( major_label, minor_label))
		ran_lis = [i for i in range(final_arr.shape[0])]
		random.shuffle(ran_lis)
		final_arr = final_arr[ran_lis]
		final_label = final_label[ran_lis]
		two_tup_lis.append( (final_arr, final_label))
	return [(tar_rest_arr_to_return, tar_rest_label_to_return), two_tup_lis]
def main():
	print( give_source_data()[0][0][:10])
	print( give_target_data()[1][0][:10])
if __name__=="__main__":
	main()
#git config --global http.proxy https://172.31.1.5:8080/