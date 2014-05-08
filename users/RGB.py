#!/usr/bin/env python

# Name: botapp_living_colors
# Author: Willy Garnier, garnie_w@yahoo.fr
# License: BSD

import time
import roslib; 
import rospy
roslib.load_manifest('aisoy_sdk_actuator')
roslib.load_manifest('aisoy_common')
from libaisoy_sdk_actuator import *;
from libaisoy_common import *

RGB=[0,0,0]
min = 0
max = 255
step = 25
speed = 0.1
actuator = Actuator()

def ChangeColor(RGB,color,min,max,step,speed):
    while (RGB[color] >= min) and (RGB[color] <= max):
        actuator. setColor(RGB[0],RGB[1],RGB[2],speed)
        RGB[color] = RGB[color] + step
    if RGB[color] > max:
        RGB[color] = max
    if RGB[color] < min:
        RGB[color] = min

def colors_sequence():
	actuator.mouthPrint("RED")
	ChangeColor(RGB,0,min,max,step,speed)
	actuator.mouthPrint("GREEN") 
	ChangeColor(RGB,1,min,max,step,speed)
	actuator.mouthPrint("BLUE") 
	ChangeColor(RGB,2,min,max,step,speed)
	actuator.mouthPrint("RED") 
	ChangeColor(RGB,0,min,max,-1*step,speed)
	actuator.mouthPrint("GREEN") 
	ChangeColor(RGB,1,min,max,-1*step,speed)

if __name__ == '__main__':
	actuator.setColor(0,255,0,1)
	while not rospy.is_shutdown():
		colors_sequence()
	
