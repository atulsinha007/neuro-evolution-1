import random
import numpy as np
#import pylab as pl

def standardize_dataset(traindata, means, stdevs):
    for row in traindata:
        for i in range(len(row)):

            row[i] = (row[i] - means[i])
            if stdevs[i]:
                row[i]/=stdevs[i]
rng=random

voweldata=np.loadtxt("vowel.csv", delimiter=',')

#rng.shuffle(voweldata) this was a big big error
numlis = np.arange(vowel.shape[0])
rng.shuffle(numlis)
vowel = vowel[ numlis ]


vowel=vowel.astype(float)
traindata=vowel
means= traindata.mean(axis=0)

stdevs=np.std(traindata,axis=0)
# standardize dataset
standardize_dataset(traindata[:,:9],means,stdevs)

def get_dimension():
    in_dem = 10
    out_dem = 11
    return (in_dem, out_dem)

def myrange(start,end,step):
    i=start
    while i+step < end:
        i+=step
        yield i
#print(traindata)

def give_data():
    #1. make iris.data in usable form
    #2. make input set and output set out of it
    #3. make setpool out of the dataset
    #4. make pcn and train it
    #5. test on validation and testing set    
    rest_setx=voweldata[:396,:10]#tuple of two shared variable of array
    rest_sety=voweldata[:396,10:]
    test_setx=voweldata[396:,:10]
    test_sety=voweldata[396:,10:]
    #print(voweldata.shape)
    #print(rest_setx.shape,test_setx.shape)
    return ((rest_setx,rest_sety),(test_setx,test_sety))

def main():
    print(give_data()[1])

if __name__ == "__main__":
    main()
