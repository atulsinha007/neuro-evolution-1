import numpy as np

def give_neg_log_likelihood( arr , oneDarr):
	parr = arr #normalize(arr,axis = 0)
	if parr.shape[1] == 1:
		 summer = np.sum([ - (oneDarr[i]*np.log(parr[i,0]+ 0.000000000001 ) + (1-oneDarr[i])*np.log(1 - parr[i,0]+0.000000000001)) for i in range(parr.shape[0]) ])
	else:
		 summer = np.sum ([ - np.log(parr[i,oneDarr[i]]+ 0.000000000001) for i in range(parr.shape[0]) ]   )
	return summer/parr.shape[0]

def give_mse(arr, oneDarr):
	if arr.shape[1]==1:
		newar = np.where(arr>0.5,1,0)
		newar = np.ravel(newar)
	else:
		newar = np.argmax(arr, axis = 1)
	#print(newar-oneDarr)
	return  np.sum((newar-oneDarr)**2)

def give_false_positive_ratio(arr, oneDarr):
	if arr.shape[1] > 2:
		print("false_positive is not appropriate objective, change objective function in Population.py")
		exit(1)
	if arr.shape[1]==1:
		ar1 = np.where(arr>0.5,1,0)
		ar1 = np.ravel(ar1)
	else:
		ar1 = np.argmax(arr, axis = 1)
	summer =  np.sum([ar1[i]*(1-oneDarr[i]) for i in range(oneDarr.shape[0])])
	dummer = np.sum([(1-ar1[i])*(1-oneDarr[i]) for i in range(ar1.shape[0])])
	return summer/(summer+dummer)

def give_false_negative_ratio(arr, oneDarr):
	if arr.shape[1] > 2:
		print("false_positive is not appropriate objective, change objective function in Population.py")
		exit(1)
	if arr.shape[1]==1:
		ar1 = np.where(arr>0.5,1,0)
		ar1 = np.ravel(ar1)
	else:
		ar1 = np.argmax(arr, axis = 1)
	summer = np.sum([(1-ar1[i])*(oneDarr[i]) for i in range(oneDarr.shape[0])])
	dummer = np.sum([(ar1[i])*(oneDarr[i]) for i in range(ar1.shape[0])])
	return summer/(summer+dummer)

def givesumar(size):
	ar = [0]
	for i in range(1, size + 1):
		ar += [ar[i - 1] + i]
	return ar