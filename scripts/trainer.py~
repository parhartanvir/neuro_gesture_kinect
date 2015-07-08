#!/usr/bin/env python
import csv
import rospy
import pickle
import os
import numpy as np
from numpy import genfromtxt
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SequentialDataSet, SupervisedDataSet,ClassificationDataSet
from pybrain.structure import SigmoidLayer, LinearLayer

rospy.init_node('trainer')

train_mat=[]

out_mat=[]


f=open('pic.pickle','rb')
dir_name=pickle.load(f)
gest_name=pickle.load(f)
n_train_ex=pickle.load(f)
n_out=pickle.load(f)
inputs=pickle.load(f)
hidden=inputs+10

print n_out
print n_train_ex
print gest_name
print hidden

out_mat=np.identity(len(gest_name))
ds=ClassificationDataSet(inputs,n_out)

for i in range(0,len(gest_name),1):
  for j in range(0,n_train_ex,1):
    name=os.path.join(dir_name,gest_name[i]+str(j+1))
    a=np.genfromtxt(name+'.csv',delimiter=',')
    
    train_mat[:]=[]
    x=a[0]
    y=a[1]
    z=a[2]
    print len(x)
    for k in range(0,len(x)-1,1):
      train_mat.append(x[k+1]-x[k])
      train_mat.append(y[k+1]-y[k])
      train_mat.append(z[k+1]-z[k])
    
    ds.addSample(train_mat,out_mat[i])

ds._convertToOneOfMany()

n=buildNetwork(inputs,hidden,hidden,n_out,hiddenclass=SigmoidLayer,bias=True)

trainer=BackpropTrainer(n,ds,momentum=0.1,weightdecay=0.01)
for _ in range(1,3000,1):
  print trainer.train()

print n.activate(train_mat)

dump_file_name=os.path.join(dir_name,'pic1.pickle')
f1=open(dump_file_name,'wb')
pickle.dump(trainer,f1)
pickle.dump(n,f1)
pickle.dump(gest_name,f1)


