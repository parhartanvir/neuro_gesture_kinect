#!/usr/bin/env python
__author__ = 'Tanvir'

import os
import rospy
import pickle
import csv
import numpy as np
from skeleton_markers.msg import Skeleton
from visualization_msgs.msg import Marker
from std_msgs.msg import String

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SequentialDataSet, SupervisedDataSet,ClassificationDataSet
from pybrain.structure import SigmoidLayer, LinearLayer

x=[]
y=[]
z=[]
gest_name=[]
mat=[]
flag=0
global x_left
global y_left
global x_right
global y_right
global x_torso
global y_torso
global z_left
global z_right
global z_torso
y_left =0.00
z_left=0.00
x_left=0.00
y_right=0.00
x_right=0.00
z_right=0.00
y_torso=0.00
x_torso=0.00
z_torso=0.00

def callback(msg):
   for joint in msg.name:           
            global st
            st=msg.name[0]
           
            p = msg.position[msg.name.index(joint)]
            global x_left
            global y_left
            global x_right
            global y_right
            global x_torso
            global y_torso
            global z_left
            global z_right
            global z_torso
            if joint=="left_hand":
              y_left=10*p.y
              x_left=10*p.x
              z_left=10*p.z
             # rospy.loginfo(joint)
            elif joint=="right_hand":
              y_right=10*p.y
              x_right=10*p.x
              z_right=10*p.z
             
            
            elif joint=="torso":
              x_torso=10*p.x
              y_torso=10*p.y
              z_torso=10*p.z

f1=open('pic1.pickle','rb')
trainer=pickle.load(f1)
n=pickle.load(f1)
gest_name=pickle.load(f1)


rospy.init_node('gesture_rec_kinect', anonymous=True)
rospy.Subscriber("/skeleton", Skeleton, callback)
pub = rospy.Publisher('/neuro_gest_kinect/gesture',String)


m=raw_input("To start entering the gesture, raise the left arm above the shoulder level. Once you bring it back down, start making the gesture with right hand. To continue press 'ENTER'")

while True:
       global x_left
       global y_left
       global x_right
       global y_right
       global x_torso
       global y_torso
       global z_right
       global z_left
       global z_torso
       
       x[:]=[]
       y[:]=[]
       z[:]=[]
       mat[:]=[]
       index=0
       if y_left>y_torso and y_right>y_torso:
         flag=0
     
       if y_left>y_torso and y_right<y_torso:
         flag=1

       if y_left<y_torso and flag==1:
         time=rospy.get_time()
         while rospy.get_time()<time+3.5:
           print x_right
           x.append(x_right)
           y.append(y_right)
           z.append(z_right)
           rospy.sleep(0.1)
         flag=0 
         all_points=[x,y,z]
         for k in range(0,len(x)-1,1):
           mat.append(x[k+1]-x[k])
           mat.append(y[k+1]-y[k])
           mat.append(z[k+1]-z[k])
         
         out = n.activate(mat)
         index=np.argmax(out)
         print index
         print out
         print "The gesture is '"+gest_name[index]+"'"
         pub.publish(gest_name[index])

