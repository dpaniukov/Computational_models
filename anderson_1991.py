#John Anderson's 1991 model
from __future__ import division
import numpy as np
from random import shuffle

# Medin & Schaffer (1978)
stims = [[1, 1, 1, 1, 1],[1, 0, 1, 0, 1],[1, 0, 1, 1, 0],[0, 0, 0, 0, 0],[0, 1, 0, 1, 1],[0, 1, 0, 0, 0]]

c=.5
alpha=1
alpha0=2
n=0
nk=[]

def pk_calc():
    pks=[]
    if len(nk)!=0:
        for part in xrange(len(nk)):
            pks.append(c*(len(nk[part]))/((1-c)+c*n))
    pks.append((1-c)/((1-c)+c*n)) #when stim is coming from an empty partition
    return pks

def pFk(stim):
    pjks=[]
    pFks=np.zeros(len(nk)+1)
    if len(nk)!=0:
        for part in xrange(len(nk)):
            diff=np.array(nk[part])-np.array(stim) #same value on a dimention where zero
            for i in xrange(len(stim)):
                cj=len(np.where(diff[:,i]==0)[0])
                pjks.append((cj+alpha)/(len(nk[part])+alpha0))
            pFks[part]=np.prod(np.array(pjks))
            pjks=[]
    for i in xrange(len(stim)):
        cj=0 #no other objects
        pjks.append((cj+alpha)/(0+alpha0)) #when stim is coming from an empty partition
    pFks[len(pFks)-1]=np.prod(np.array(pjks))
    pjks=[]
    return pFks

def simulate(stim):    
    pks=pk_calc()
    pFks=pFk(stim)
    probs=pFks*np.array(pks)
    winner=np.argmax(probs)
    if (len(nk)-1)<winner:
        nk.append([])
    nk[winner].append(stim)
    print "Stim: ",stim
    print "Partitions: ",nk
    print "Prob: ",probs
    return

#shuffle(stims)    
for s in xrange(len(stims)):
    stim=stims[s]
    simulate(stim)
    n+=1
        