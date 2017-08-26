#misc.py
import numpy as np
def binsear(p,arr):
	
	low=0
	high=len(arr)-1
	while (high-low)>1:
		mid=arr[(low+high)//2]
		if mid>p:
			high=(low+high)//2
		else:
			low=(low+high)//2
	return low#this is the index of our chosen in poparr



def RoulWheel(arr):
	sumarr=[0]
	for i in range(len(arr)):
		sumarr.append(sumarr[i]+arr[i])
	n=len(arr)//2
	for j in range(n):
		r = np.random.uniform(0, sumarr[-1],2)
		chosenind1=binsear(r[0],sumarr)
		chosenind2=binsear(r[1],sumarr)
		yield (chosenind1,chosenind2)
def WeighRoulWheel(popul):
	ar=popul.find_expecarr()
	for tup   in   RoulWheel(ar):
			yield popul.poparr[tup[0]],popul.poparr[tup[1]]


	
def RankRoulWheel(popul):
	ar=np.arange(0,popul.size)
	listup=list(zip(list(popul.poparr),list(popul.fitarr)))
	listup.sort(key=lambda x: x[1])
	for  tup in RoulWheel(ar):
		yield listup[tup[0]][0],listup[tup[0]][0]

def middlepoint(parent_tup):
	alpha=np.random.uniform(0,1)
	child1=alpha*parent_tup[0]+(1-alpha)*parent_tup[1]
	child2=alpha*parent_tup[1]+(1-alpha)*parent_tup[0]
	return (child1,child2)

def smallchange(newborn):
	return newborn+np.random.normal(-1,1,newborn.shape)/5



class Selection:
	def __init__(self,typeh=0):
		self.type=typeh
		
	def select_parent(self,popul):
		if self.type==0:
			return WeighRoulWheel(popul)	#takes in population, returns a tuple of two vectors
		elif self.type==1:
			return RankRoulWheel(popul)
		elif self.type==2:
			#use alitism
			return None

class Crossover:
	def __init__(self,typeh=0,rate=1,stadym=0):
		self.type=typeh
		self.rate=rate
		self.stadym=stadym

	def do_crossover(self,parent_tup):
		if np.random.rand()<self.rate:

			if self.type==0:
				return middlepoint(parent_tup)	#returns a tuple of children(vectors)

			elif self.type==1:
				return singlepoint()	
			elif self.type==2:
				return 
			elif self.type==3:
				#use alitism
				return None

class Mutation:
	def __init__(self,typeh=0,rate=0.1,stadym=0):
		self.type=typeh
		self.rate=rate
		self.stadym=stadym

	def mutate(self,newborn):
		if np.random.rand()<self.rate:

			if self.type==0:
				return smallchange(newborn)	#returns a children (vector)

			elif self.type==1:
				return None
		else:
			return newborn
class Termination:
	def __init__(self,typeh=0):
		self.type=typeh
	def terminate(self,generationnum=None,generationlim=100):
		if  self.type==0:
			if generationnum>generationlim:
				return  1
			else:
				return  0

		elif   self.type==1:

			pass
