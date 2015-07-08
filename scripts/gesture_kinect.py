#!/usr/bin/env python
__author__ = 'Tanvir'

import os
import rospy
import pickle
import csv
import rospy
from skeleton_markers.msg import Skeleton
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from std_msgs.msg import String

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SequentialDataSet, SupervisedDataSet,ClassificationDataSet
from pybrain.structure import SigmoidLayer, LinearLayer



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
pose=Twist()
st=String()
lt=String()
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
              
            

   #rospy.loginfo(m)
    

  
rospy.init_node('get_gesture_kinect')
rospy.Subscriber("/skeleton", Skeleton, callback)
global x_left
global y_left
global x_right
global y_right
global x_torso
global y_torso
global z_right
global z_left
global z_torso
lt="left_hand"
r = rospy.Rate(10) # 10hz
dir_name=raw_input('Please put the directory of the folder where you would like to store the datasets :')
x=[]
y=[]
z=[]
gest_name=[]

rospy.Subscriber("/skeleton", Skeleton, callback)

n_out=input('Please type the number of gestures:')
n_train_ex =input('Please type the number of training examples you want to give (10 to 15 would be a reasonable chioce):')

while True:
  gest_name[:]=[]
  for i in range(0,n_out,1):
   
   gesture=raw_input("please enter the name for gesture number "+str(i+1)+" : ")
   gest_name.append(gesture)
   
  print "The gestures are :"
  print gest_name
  fine=raw_input("is it fine? (Y/N) ")
  if fine=="y" or fine=="Y":
    break

print "OK! The gestures are :"
print gest_name
print "   "
m=raw_input("To start entering the data_sets, raise the left arm above the shoulder level. Once you bring it back down, start making the gesture with right hand. To continue press 'ENTER'")

for l in range(0,len(gest_name),1):
 for k in range(0,n_train_ex,1):
  x[:]=[]
  y[:]=[]
  z[:]=[]
  flag=0
  print "Waiting to record dataset number "+str(k+1)+"  for '"+ gest_name[l]+"'"
   
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
       if y_left>y_torso and y_right>y_torso:
         flag=0
     
       if y_left>y_torso and y_right<y_torso:
         flag=1

       if y_left<y_torso and flag==1:
         time=rospy.get_time()
         while rospy.get_time()<time+3.5:
           
           x.append(x_right)
           y.append(y_right)
           z.append(z_right)
           rospy.sleep(0.1)
         flag=0 
         all_points=[x,y,z]
         inputs=(len(x)-1)*3
         
         break
   
  file_name=gest_name[l]+str(k+1)
  full_file_name=os.path.join(dir_name,file_name+'.csv')
  with open(full_file_name, 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(all_points) 

print "OK! The data has been recorded. Just give me a moment to save the variables"
#path=raw_input("Please enter the path to your package : ")
pickle_file=os.path.join(dir_name,'pic.pickle')
f=open(pickle_file,'wb')
pickle.dump(dir_name,f)
pickle.dump(gest_name,f)
pickle.dump(n_train_ex,f)
pickle.dump(n_out,f)
pickle.dump(inputs,f)     
      

      
 


