#ALCOVE 1992. Replicating Shepard et al. (1961) simulation

from __future__ import division
import numpy as np
import pylab

np.set_printoptions(suppress=True)

#constants
#lambda_att = 0.0
lambda_att = .0033
lambda_wt = .03
r = 1
q = 1
c=6.5
phi=3.0
epochs=50

#exemplars and categories
exemplars=np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])
cat_type1=np.array(['A','A','A','A','B','B','B','B'])
cat_type2=np.array(['A','B','A','B','B','A','B','A'])
cat_type3=np.array(['A','B','A','A','A','B','B','B'])
cat_type4=np.array(['A','B','A','A','B','B','A','B'])
cat_type5=np.array(['A','B','A','A','B','A','B','B'])
cat_type6=np.array(['B','A','A','B','A','B','B','A'])
categories = [cat_type1,cat_type2,cat_type3,cat_type4,cat_type5,cat_type6]
exemp_pos=np.array([0,1,2,3,4,5,6,7]) #this will be used to shuffle exemplars, but still be albe to correspond them with category labels
pr_cor_categ=[]

def update(stim):
    act_hid = np.exp(-c*(np.sum(att*np.abs(exemplars-stim), axis=1)))
    act_A_out=np.sum((wt[0]*act_hid),axis=0)
    act_B_out=np.sum((wt[1]*act_hid),axis=0)
    act_all_out=np.array([[act_A_out],[act_B_out]])
    
    return [act_hid,act_A_out,act_B_out,act_all_out]
    

for cat in range(len(categories)):
        
    att = np.array([1/3,1/3,1/3])
    wt = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
    pr_cor_epoch=[] #for output
            
    for ep in range(50):
        error_trials=[]
        dwt_trials=np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
        datt_trials=np.array([0,0,0])
        np.random.shuffle(exemp_pos)
        
        for ex in range(len(exemplars)):
            stim=exemplars[exemp_pos[ex]]
            cat_type=categories[cat]
            act_hid = update(stim)[0]

            act_A_out=update(stim)[1]
            act_B_out=update(stim)[2]
            act_all_out=update(stim)[3]
        
            if cat_type[exemp_pos[ex]] == 'A':
                teacher=np.array([[max(1,act_A_out)],[min(0,act_B_out)]])
            elif cat_type[exemp_pos[ex]] == 'B':
                teacher=np.array([[min(0,act_A_out)],[max(1,act_B_out)]])

            att_error=np.array([[(np.sum(((teacher-act_all_out)*wt),axis=0)*act_hid)][0],]*len(stim))*(c*np.abs(exemplars-stim)).transpose()
            delta_att=-lambda_att*np.sum(att_error, axis=1)
            
            delta_wt=lambda_wt*(teacher-act_all_out)*act_hid
            
            wt=wt+delta_wt
            att=att+delta_att
            for i in range(len(att)):
                if att[i] < 0:
                    att[i]=0        
        
        #update for the graph
        for ex in range(len(exemplars)):
            stim=exemplars[exemp_pos[ex]]
            cat_type=categories[cat]

            act_A_out=update(stim)[1]
            act_B_out=update(stim)[2]
            act_all_out=update(stim)[3]

            prA=np.exp(phi*act_A_out)/np.sum(np.exp(phi*act_all_out), axis=0)
            prB=np.exp(phi*act_B_out)/np.sum(np.exp(phi*act_all_out), axis=0)
            
            error=[]
            if cat_type[exemp_pos[ex]] == 'A':
                error=[abs(1-prA),abs(0-prB)]
            elif cat_type[exemp_pos[ex]] == 'B':
                error=[abs(0-prA),abs(1-prB)]
            error_trials+=error

        pr_cor_epoch.append(np.sum(error_trials)/len(error_trials))

    pr_cor_categ.append(pr_cor_epoch)

#show the graph
pylab.ioff() # Turn off interactive mode.
pylab.hold(True)
pylab.figure()
plots1 = [pylab.plot(range(len(pat)), [1-p for p in pat], \
    label='Task '+str(j+1)) for j,pat in enumerate( pr_cor_categ )]
pylab.title( "Dmitrii. With attention increase" )
pylab.xlabel("Epochs, n= %s" % str(epochs * len(exemplars)) )
pylab.ylabel("Percent correct")
pylab.ylim((.5,1.))
pylab.legend(loc=0)
pylab.show()
