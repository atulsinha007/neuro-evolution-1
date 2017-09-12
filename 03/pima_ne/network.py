#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 15:21:12 2017

@author: adi
"""

import numpy as np

def sigmoid(arr):
	return 1/(1+np.exp(-arr))

class Network:	
	def __init__(self,inputdim,outputdim,arr_of_net,trainx,trainy,testx,testy):
		"""trainx=trainarr[:,:inputdim]
		trainy=trainarr[:,inputdim:]
		testx=testarr[:,:inputdim]
		testy=testarr[:,inputdim:]
		"""
		self.inputdim=inputdim
		self.outputdim=outputdim
		self.trainx = trainx
		self.trainy = trainy
		self.testx = testx 
		self.testy = testy
		self.arr_of_net=arr_of_net
		#self.hid_nodes=hid_nodes

	def feedforward(self):
        
		#weight_arr = np.array(weight_arr)
		#arr_of_net  type: nd.array, it is a whole list of network (i.e. each vector is a new network with hid_nodes)
		lis=[]
		for i in range(self.arr_of_net.shape[0]):
			hid_nodes=int(self.arr_of_net[i][0])
			fir_weight=self.arr_of_net[i][1:(self.inputdim+1)*hid_nodes+1].reshape(self.inputdim+1,hid_nodes)
			sec_weight=self.arr_of_net[i][(self.inputdim+1)*hid_nodes+1:].reshape(hid_nodes+1,self.outputdim)
			trainx = np.concatenate((self.trainx,-np.ones((self.trainx.shape[0],1))),axis=1)
			midout = np.dot(trainx,fir_weight)
			midout = sigmoid(midout)
			midout = np.concatenate((midout, -np.ones((midout.shape[0],1))), axis=1)
			output = np.dot(midout, sec_weight)
			output = sigmoid(output)
			er_arr = (1/2)*np.mean((output-self.trainy)**2)
			lis.append(er_arr)
		return np.array(lis)
			

           
            
            
            
            
            

	def test(self,weight_arr):
		hid_nodes=int(self.arr_of_net[i][0])
		fir_weight = weight_arr[1:(self.inputdim+1)*hid_nodes+1].reshape(self.inputdim+1,hid_nodes)
		sec_weight = weight_arr[(self.inputdim+1)*hid_nodes+1:].reshape((hid_nodes+1),self.outputdim)
		testx = np.concatenate((self.testx,-np.ones((self.testx.shape[0],1))),axis=1)
		midout = np.dot(testx,fir_weight)
		midout = sigmoid(midout)
		midout = np.concatenate((midout,-np.ones((midout.shape[0],1))),axis=1)
		output = np.dot(midout,sec_weight)
		output = sigmoid(output)
		er_arr = (1/2)*np.mean((output-self.testy)**2)
		return er_arr
        

def squa_test(x):
	return (x**2).sum(axis=1)

def main():
	#print("hi")
	import copy
	trainarr = np.concatenate((np.arange(0,9).reshape(3,3),np.array([[1,0],[0,1],[1,0]])),axis=1)
	testarr = copy.deepcopy(trainarr)
	trainx=trainarr[:,:3]
	trainy=trainarr[:,3:]
	testx=testarr[:,:3]
	testy=testarr[:,3:]
	size=5
	indim = 3
	outdim = 2
	hidarr=np.random.randint(1,4,(size))
	lis=[]
	for i in hidarr:
		lis.append(np.concatenate((np.array([i]),np.random.uniform(-1,1,(indim+1)*i+(i+1)*outdim))))
	arr_of_net=np.array(lis)
	print(arr_of_net)
	net = Network(3,2,arr_of_net,trainx,trainy,testx,testy)
	print(net.trainx,net.trainy)
	#hid_nodes = 4

	#size = 5
	
	print(net.arr_of_net)
	print(net.feedforward())
if __name__ == '__main__':
	main()