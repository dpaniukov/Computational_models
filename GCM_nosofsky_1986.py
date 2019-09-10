import numpy as np
from math import exp

category =['1']*8
category.extend('2'*8)
category=np.array(category)

#Subject 1
exemplars=np.array([[-1.855,-1.532],[-.687,-1.617],[.436,-1.633],[1.331,-1.647],[-1.615,-.469],[-.531,-.558],[.500,-.590],[1.373,-.535],[-1.522,.657],[-.395,.518],[.648,.469],[1.513,.481],[-1.427,1.770],[-.301,1.639],[.767,1.541],[1.764,1.512]])

#Subject 1
c=1.099
w=.0001
b=.444

for i in range(len(exemplars)):

    stim=exemplars[i]
    dists=(stim-exemplars)**2
    sims=np.array(np.exp(-(c**2)*(w*(dists[:,0])+(1-w)*(dists[:,1]))))
    simA=b*sum(sims[np.where(category=='1')[0]])
    simB=(1-b)*sum(sims[np.where(category=='2')[0]])

    prA=simA/(simA+simB)
    print prA
    #print max([prA,1-prA])
    
