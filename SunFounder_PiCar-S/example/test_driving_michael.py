#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
**********************************************************************
* Filename    : ultra_sonic_avoidance.py
* Description : An example for sensor car kit to followe light
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-27    New release
**********************************************************************
'''

from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import time
import picar
import random
import math
from numpy import arange,array,ones,linalg
import numpy as np


length_correction_array = 7

#helper functions
def get_m_from_linear_regression():

	xi = arange(0,7)
	A = array([ xi, ones(length_correction_array)])
	# linearly generated sequence
	y = right_wall_distance
	w = linalg.lstsq(A.T,y)[0] # obtaining the parameters
	
	return round(w[0],2)

def append_distance_for_correction(dist):

	if (len(right_wall_distance) >= length_correction_array):
		median = np.median(right_wall_distance)
		for el in right_wall_distance:
			if (abs(el - median)) > 10:
 				right_wall_distance.pop(el)
	right_wall_distance.append(dist)
		


#basic car functions
class back_wheels_shabi(back_wheels.Back_Wheels):

    def turn_right(self):
        ''' Move left backwards and right forwards '''

        self.left_wheel.backward()
        self.right_wheel.forward()
        if self._DEBUG:
            print self._DEBUG_INFO, 'Turning left'

    def turn_left(self):
        ''' Move left backwards and right forwards '''

        self.left_wheel.forward()
        self.right_wheel.backward()
        if self._DEBUG:
            print self._DEBUG_INFO, 'Turning left'



#picar.setup()


right_wall_distance = []


ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')

# bw = back_wheels.Back_Wheels(db='config')

bw = back_wheels_shabi()
fw.turning_max = 90

cell_length = 40.64


global_forward_speed = 0
global_backward_speed = 80

back_distance = 10
turn_distance = 1

timeout = 10
last_angle = 90
last_dir = 0

delay = .2  # delay for front servo

right_thresh = 30
left_thresh = 30
front_thresh = 30



def get_sensor_readings():

    def turn_sensor(dir):
        if dir == 'left':
            fw.turn(180)
            time.sleep(delay)
        if dir == 'center':
            fw.turn(90)
            time.sleep(delay)
        if dir == 'right':
            fw.turn(0)
            time.sleep(delay)

    # turn the sensor to three different positions and get distance measure from each

    center = ua.get_distance()
    turn_sensor('left')
    left = ua.get_distance()
    turn_sensor('right')
    time.sleep(0.1)
    right = ua.get_distance()
    turn_sensor('center')

    return {'left': left, 'center': center, 'right': right}


def move(direction):

    if(direction == "forward"):
	print("Moving one cell")
   	starting_distance = ua.get_distance()
    	while((starting_distance - ua.get_distance()) <= cell_length):
		print(ua.get_distance())
		bw.left_wheel.backward()
		bw.right_wheel.backward()
		bw.left_wheel.speed = global_forward_speed
		bw.right_wheel.speed = global_forward_speed
	
    elif(direction == "backward"):
	print("Backing up")
	starting_distance = ua.get_distance()
    	while((ua.get_distance() - starting_distance) <= cell_length):
		bw.left_wheel.forward()
		bw.right_wheel.forward()
		bw.left_wheel.speed = 60
		bw.right_wheel.speed = 60
   
    elif(direction == "left"):
	print("turning left")
	bw.left_wheel.backward()
	bw.right_wheel.backward()
	bw.left_wheel.speed = 73
	bw.right_wheel.speed = 31
	time.sleep(2.0)
	starting_distance = ua.get_distance()
    	while((ua.get_distance() - starting_distance) <= 12):
		bw.left_wheel.forward()
		bw.right_wheel.forward()
		bw.left_wheel.speed = 60
		bw.right_wheel.speed = 60

    elif(direction == "right"):
	print("turning right")
	bw.left_wheel.backward()
	bw.right_wheel.backward()
	bw.left_wheel.speed = 31
	bw.right_wheel.speed = 73
	time.sleep(2.0)
	starting_distance = ua.get_distance()
    	while((ua.get_distance() - starting_distance) <= 12):
		bw.left_wheel.forward()
		bw.right_wheel.forward()
		bw.left_wheel.speed = 60
		bw.right_wheel.speed = 60

def move_time(sec):
    start = time.time()
    while((start + sec) > time.time()):
    
	left_speed, right_speed = correct_speed()
    	
	bw.left_wheel.backward()
    	bw.right_wheel.backward()
	bw.left_wheel.speed = left_speed
    	bw.right_wheel.speed = right_speed

def turn_sensor_right():
    fw.turn(0)
    time.sleep(0.2)

def slight_turn():
    bw.left_wheel.backward()
    bw.right_wheel.backward()
    bw.left_wheel.speed =  10
    bw.right_wheel.speed = 80
    time.sleep(0.2)
   
def correct_speed():
    distance = ua.get_distance()
    print(distance)

    append_distance_for_correction(distance) 

    if(len(right_wall_distance) < 7):
    	return global_forward_speed, global_forward_speed
    m = get_m_from_linear_regression()
    print("m: ", m)
    k = 2

    left_speed = int(global_forward_speed * (1 - k * abs(m) * m))
    right_speed = int(global_forward_speed * (1 + k * abs(m) * m))
    
    return max(min(left_speed, 100),0), max(min(right_speed, 100),0)

def start_testdrive():
    turn_sensor_right()
    move_time(2.5) #
    print 'start_testdrive'
    stop()

def stop():
    bw.stop()
    fw.turn_straight()



if __name__ == '__main__':
    try:
	
	start_testdrive()
	print(right_wall_distance)

	
    except KeyboardInterrupt:
        stop()

			
