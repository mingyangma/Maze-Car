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

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')

# bw = back_wheels.Back_Wheels(db='config')

bw = back_wheels_shabi()
fw.turning_max = 90

cell_length = 40.64

forward_speed = 50
backward_speed = 60

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
		bw.left_wheel.speed = 50
		bw.right_wheel.speed = 50
	
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
    	bw.left_wheel.backward()
    	bw.right_wheel.backward()
    	bw.left_wheel.speed = 50
    	bw.right_wheel.speed = 50
	dist = ua.get_distance()
	correct(dist)

def turn_sensor_right():
    fw.turn(0)
    time.sleep(0.2)

def slight_turn():
    bw.left_wheel.backward()
    bw.right_wheel.backward()
    bw.left_wheel.speed =  10
    bw.right_wheel.speed = 80
    time.sleep(0.2)
   
def correct(dist):
    if(dist > 13):
	slight_turn()

def start_testdrive():
    turn_sensor_right()
    move_time(3)
    print 'start_testdrive'
    stop()

def stop():
    bw.stop()
    fw.turn_straight()


if __name__ == '__main__':
    try:
	start_testdrive()
    except KeyboardInterrupt:
        stop()

			
