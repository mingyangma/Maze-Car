# import numpy as np
import copy
from sys import stdout
import numpy as np


###############################################################################
class CELL:
    def __init__(self, cell_no = 25, open_dir = []):
        self.cell_no = cell_no
        self.openings = open_dir

###############################################################################
class PATH:
    def __init__(self, cell):
        self.path = [cell]
        self.visited_cells = ["00000", "00000", "00100"]
        self.exit_cells = [1, 2, 3, 4, 5, 6, 7,
                           8, 14, 15, 21, 22, 28]

    def add_visited(self, cell_no):
        no = cell_no
        row_idx = np.int(np.round(no/7))-2
        col_idx = (no-1)%7 -1
        row = self.visited_cells[row_idx]
        visited = list(row)
        visited[col_idx] = "1"
        self.visited_cells[row_idx] = "".join(visited)

    def check_bingo_and_update_exit_cells(self):
        for row_no, row in enumerate(self.visited_cells):
            if "111" in row:
                bingo_starting_idx = row.find("111")

                if bingo_starting_idx == 0:
                    self.exit_cells.extend([12, 19, 26])
                elif bingo_starting_idx == 1:
                    self.exit_cells.extend([9, 16, 23, 13, 20, 13, 20, 27])
                elif bingo_starting_idx == 2:
                    self.exit_cells.extend([10, 17, 24])
                return(bingo_starting_idx)

        return False

    def mark_map_end(self, cell_no, cell_dir):
        no = cell_no
        col_idx = (no-1)%7
        row_idx = np.int(np.round(no/7))-1

    def check_exit_avail(self, curr_cell, avail_opens):
        possible_exit_cells = {}

        for open_dir in avail_opens:
            if open_dir == 0:
                next_cell = curr_cell - 7
                possible_exit_cells[next_cell] = 0
            elif open_dir == 2:
                next_cell = curr_cell + 7
                possible_exit_cells[next_cell] = 2
            elif open_dir == 1:
                next_cell = curr_cell + 1
                possible_exit_cells[next_cell] = 1
            elif open_dir == 3:
                next_cell = curr_cell - 1
                possible_exit_cells[next_cell] = 3
        print("POSSIBLE MOVES: {}".format(possible_exit_cells))
        print("POSSIBLE EXITS: {}".format(self.exit_cells))

        for next_cell, direction in possible_exit_cells.iteritems():
            print(next_cell)
            if next_cell in self.exit_cells:
                print("FOUND EXIT!")
                print("EXITTING TO: {} {}".format(next_cell, direction))
                return direction
        return False


    def print_path(self):
        stdout.write('>>>  START - ')
        for cell in self.path:
            stdout.write('[CELL_NO:{} OPENS:{}] - '.format(cell.cell_no, cell.openings))
        stdout.write(' END \n')

    def append_cell(self, cell):
        self.path.append(cell)

    def most_recent_cell(self):
        cell = self.path[-1]
        return cell

    def delete_opening(self, opening):
        new_open = []
        old_open = copy.deepcopy(self.path[-1].openings)
        for i in old_open:
            if i != opening:
                new_open.append(i)
        self.path[-1].openings = new_open
        print("DELETING {}".format(opening))

    def pop_cell(self):
        return self.path.pop()

################################################################################
# Forward: same_heading, Backward: same_heading
# Right (+1), Left(-1)
# N(0) W()

class BOT:
    def __init__(self, curr_loc = 25, heading = 0):
        self.prev_cell_no = -1
        self.curr_cell_no = curr_loc
        self.heading = heading
	self.prev_heading = 0

    def dest_cell_no(self, direction):
        current_cell_no = self.curr_cell_no

        if direction == 0:
            dest_cell_no = current_cell_no - 7
        elif direction == 1:
            dest_cell_no = current_cell_no + 1
        elif direction == 2:
            dest_cell_no = current_cell_no + 7
        elif direction == 3:
            dest_cell_no = current_cell_no - 1

        return dest_cell_no

    def forward_move(self, from_cell, to_cell):
        bot_heading = self.heading
        diff = to_cell - from_cell

        if diff == -7:
            move_dir = 0
        elif diff == 7:
            move_dir = 2
        elif diff == 1:
            move_dir = 1
        elif diff == -1:
            move_dir = 3

        print("DIFF:  {}".format(move_dir - bot_heading))
        print("BOT PREV HEADING {}".format(self.heading))
        if abs(move_dir - bot_heading) == 0:
            # move_forward_method()
            self.prev_heading = self.heading
            move("forward")
            self.heading = self.heading
            print("MOVEVING FORWARD")
        elif abs(move_dir - bot_heading) == 2:
            # move_backward_method()
            self.prev_heading = self.heading
            move("backward")
            self.heading = self.heading
            print("MOVEVING BACKWARD")
        elif move_dir - bot_heading == 1 or move_dir - bot_heading == -3:
            # move_right_method()
            self.prev_heading = self.heading
            move("right")
            self.heading = (self.heading + 1) % 4
            print("MOVEVING FORWARD-RIGHT")
        elif move_dir - bot_heading == -1 or move_dir - bot_heading == 3:
            self.prev_heading = self.heading
	    move("left")
            self.heading = (self.heading - 1) % 4
            print("MOVEVING FORWARD-LEFT")
            # move_left_method()

        print("BOT CURR HEADING {}".format(self.heading))

        self.prev_cell_no = from_cell
        self.curr_cell_no = to_cell

    def revert_move(self, from_cell, to_cell):
	prev_bot_heading = self.prev_heading
        bot_heading = self.heading

        turn_diff = prev_bot_heading - bot_heading

        print("TURN DIFF:  {}".format(turn_diff))
        print("BOT PREV HEADING {}".format(self.heading))
        if turn_diff == -3 or turn_diff == 1:
            move("back_left")
            self.heading = self.prev_heading
            print("MOVEVING BACKWARD-LEFT")
        elif turn_diff == 3 or turn_diff == -1:
            move("back_right")
            self.heading = self.prev_heading
            print("MOVEVING BACKWARD-RIGHT")
        elif turn_diff == 0 or abs(turn_diff) == 2:
            move("back")
            self.heading = self.heading
            print("MOVEVING BACKWARD")


        print("BOT CURR HEADING {}".format(self.heading))

        self.prev_cell_no = from_cell
        self.curr_cell_no = to_cell


    def take_measurements(self):
		bot_heading = self.heading
		right = (bot_heading + 1)%4
		center = bot_heading
		left = (bot_heading - 1)%4
 	
		msmt = []
		thresh = 30
		sensor_readings = get_sensor_readings()
		print(sensor_readings)
		if sensor_readings["right"] > thresh:
		    msmt.append(right)	
		if sensor_readings["center"] > thresh:
		    msmt.append(center)
		if sensor_readings["left"] > thresh:
		    msmt.append(left)	
		print("SENSOR MSMT: {}".format(msmt))    
		return msmt



 ################################################################################

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
import collections
import math
from numpy import arange,array,ones,linalg
import numpy as np

#helper functions

length_correction_array = 7
length_correction_array_to_start = 5


def get_m_from_linear_regression():

	xi = arange(0, len(right_wall_distance))
	A = array([ xi, ones(len(right_wall_distance))])
	# linearly generated sequence
	
	y = []
	median = np.median(right_wall_distance)
	for el in right_wall_distance:
		if(abs(el - median) < 5):
			y.append(el)
	print(len(y))
	y = right_wall_distance
	w = linalg.lstsq(A.T,y)[0] # obtaining the parameters
	
	return round(w[0],2)

def check_walls():
    bot_head = test_bot.heading
    no_walls = test_path.most_recent_cell().openings
    wall = []
    if (bot_head + 1)%4 not in no_walls:
    	wall.append("R")
    if (bot_head - 1)%4 not in no_walls:
    	wall.append("L")
    return wall

def stop():
    bw.stop()
    fw.turn_straight()

#basic car functions

picar.setup()

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


right_wall_distance = collections.deque(maxlen=length_correction_array)


ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')

# bw = back_wheels.Back_Wheels(db='config')

bw = back_wheels_shabi()
fw.turning_max = 90

cell_length = 40.64


global_forward_speed = 50
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
	
	move_time(1.75)
	
	
    elif(direction == "backward"):
	print("Backing up")

	turn_sensor_right()
	move_time_backward(0.8)
	turn_sensor_straight()
   
    elif(direction == "left"):
	print("turning left")
	bw.left_wheel.backward()
	bw.right_wheel.backward()
	bw.left_wheel.speed = 100
	bw.right_wheel.speed = 15
	time.sleep(0.9)
	
	bw.left_wheel.speed = 80
	bw.right_wheel.speed = 80
	time.sleep(0.13)
    	

    elif(direction == "right"):
	print("turning right")
	bw.left_wheel.backward()
	bw.right_wheel.backward()
	bw.left_wheel.speed = 20
	bw.right_wheel.speed = 90
	time.sleep(1.05)

	bw.left_wheel.speed = 80
	bw.right_wheel.speed = 80
	time.sleep(0.15)

    elif(direction == "back_left"):
	print("turning back left")
	bw.left_wheel.forward()
	bw.right_wheel.forward()
	bw.left_wheel.speed = 100
	bw.right_wheel.speed = 45
	time.sleep(1.18)

	bw.left_wheel.backward()
	bw.right_wheel.backward()
	bw.left_wheel.speed = 80
	bw.right_wheel.speed = 80
	time.sleep(0.22)

    elif(direction == "back_right"):
	print("turning back right")
	bw.left_wheel.forward()
	bw.right_wheel.forward()
	bw.left_wheel.speed = 45
	bw.right_wheel.speed = 100
	time.sleep(1.18)

	bw.left_wheel.backward()
	bw.right_wheel.backward()
	bw.left_wheel.speed = 80
	bw.right_wheel.speed = 80
	time.sleep(0.22)        


    stop()	

def move_time(sec):
	

    right_correction = 1
    correction_time_interval = sec - 0.5

    start = time.time()

    walls = check_walls()
    
    if("R" in walls):
	turn_sensor_right()
    	while((start + sec) > time.time()):
    
		left_speed, right_speed = correct_speed()
    	
		bw.left_wheel.backward()
    		bw.right_wheel.backward()
		
		if((start + correction_time_interval) > time.time()):
			bw.left_wheel.speed = left_speed + right_correction
    			bw.right_wheel.speed = right_speed
		else:
			bw.left_wheel.speed = global_forward_speed + right_correction
    			bw.right_wheel.speed = global_forward_speed
    
    elif("L" in walls):
	turn_sensor_left()
    	while((start + sec) > time.time()):
    
		left_speed, right_speed = correct_speed()
    	
		bw.left_wheel.backward()
    		bw.right_wheel.backward()

		if((start + correction_time_interval) > time.time()):
			bw.left_wheel.speed = right_speed #must be inverted because of left view instead of right
    			bw.right_wheel.speed = left_speed + right_correction
		else:
			bw.left_wheel.speed = global_forward_speed 
    			bw.right_wheel.speed = global_forward_speed + right_correction

    else:
    	while((start + sec) > time.time()):
		bw.left_wheel.backward()
    		bw.right_wheel.backward()
		bw.left_wheel.speed = global_forward_speed + right_correction
    		bw.right_wheel.speed = global_forward_speed

    turn_sensor_straight()

def move_time_backward(sec):
    start = time.time()
    while((start + sec) > time.time()):
    	
	bw.left_wheel.forward()
    	bw.right_wheel.forward()
	bw.left_wheel.speed = global_backward_speed
    	bw.right_wheel.speed = global_backward_speed


def turn_sensor_right():
    fw.turn(0)
    time.sleep(0.2)

def turn_sensor_left():
    fw.turn(180)
    time.sleep(0.2)


def turn_sensor_straight():
    fw.turn(90)
    time.sleep(0.2)
   
def correct_speed():
    distance = ua.get_distance()
    print(distance)

    right_wall_distance.append(distance)

    if(len(right_wall_distance) < length_correction_array_to_start):
    	return global_forward_speed, global_forward_speed
    m = get_m_from_linear_regression()
    m = max(min(m, 0.75),-0.75)
    print("m: ", m)

    k = 1.0

    left_speed = int(global_forward_speed * (1 - k * abs(m) * m))
    right_speed = int(global_forward_speed * (1 + k * abs(m) * m))
    
    return max(min(left_speed, 100),0), max(min(right_speed, 100),0)

def start_testdrive():
    #turn_sensor_right()
    #move_time(1.82) #
    #print 'start_testdrive'
    move("back_right")
    stop()
			


################################################################################
# START GAME
iter_cnt = 0
test_bot = BOT()
bot_position = test_bot.curr_cell_no
print("BOT STARTING IN CELL:  {}\n\n".format(bot_position))

sensor_measurements = test_bot.take_measurements()
print("BOT POSSIBLE MOVES:    {}".format(sensor_measurements))

new_cell = CELL(bot_position, open_dir = sensor_measurements)
test_path = PATH(new_cell)
test_path.print_path()

try:
	while -1 not in sensor_measurements:
	    iter_cnt += 1
	
	    # CASE - Dead-end: REVERTING IN CASE OF ENCOUNTERING DEAD END.
	    while len(sensor_measurements) == 0:
	        # First mark the dead-end as dead-cell for current location
	        print("\t*****======>{}<======*****".format(iter_cnt))
	        print("\tBOT REVERTING MOVES!")
	        # Pop out the most recently added cell(dead-end) and take current bot location.
	        current_cell = test_path.pop_cell()
	        bot_position = current_cell.cell_no
	        print("\tBOT REVETTING FROM CELL  {}".format(bot_position))
	
	        # Grabbing the cell before the dead-end and cell number.
	        revert_cell = test_path.most_recent_cell()
	        revert_cell_no = revert_cell.cell_no
	        print("\tBOT REVERTING TO:        {}".format(revert_cell_no))
	
	        # Revert from dead-end to the previous cell.
	        test_bot.revert_move(bot_position, revert_cell_no)
	        print("\tBOT COMPLETED MOVING")
	
	        # Grab the bot's current cell number
	        bot_position = test_bot.curr_cell_no
	        bot_heading = test_bot.heading
	        print("\tBOT NOW IN CELL:         {}".format(bot_position))
	        print("\tBOT HEADING IS :         {}".format(bot_heading))
	
	        # Print out the path and x-map
	        stdout.write("\t")
	        test_path.print_path()
	
	        # Grab new sensor measurements to find another opening.
	        sensor_measurements = test_path.most_recent_cell().openings
	        iter_cnt +=1
	        print("\t*****======*****======*****\n")
		

	    # CASE - No dead-end
	    print("===========>{}<=============".format(iter_cnt))
	    print("BOT MOVING FROM CELL:    {}".format(test_bot.curr_cell_no))
	    print("BOT POSSIBLE MOVES:      {}".format(sensor_measurements))
	
	    # Pick one direction from MANY: HERE using the logic that moving forward to the same direction is least error-prone
	    # Also assuming sensor measurement is taken by [Center, Left, Right]
	    exit_dir = test_path.check_exit_avail(test_bot.curr_cell_no, sensor_measurements)
	    if type(exit_dir) == int:
	        move_to_dir = exit_dir
	        print("MOVE TO DIRECTION SET AS {}".format(move_to_dir))
	    elif type(exit_dir) == bool:
	        move_to_dir = sensor_measurements[0]
	
	    # Get the cell number that results from moving one cell to the selectd direction.
	    print("BOT TAKING DIRECTION:    {}".format(move_to_dir))
	    dest_cell = test_bot.dest_cell_no(move_to_dir)
	
	    print("BOT MOVING TO CELL:      {}".format(dest_cell))
	
	
	
	    # First delete the direction from the possible direction list
	    test_path.delete_opening(move_to_dir)
		
	    test_bot.forward_move(test_bot.curr_cell_no, dest_cell)
	    if type(exit_dir) == int:
	        print("Game Done")
	        break
	    ### NEW*
	    test_path.add_visited(dest_cell)
	    ### NEW* Check for "Bingo"
	    test_path.check_bingo_and_update_exit_cells()
	
	    print("BOT COMPLETED MOVING")
	
	    # Print the cell number after bot moving
	    bot_position = test_bot.curr_cell_no
	    bot_heading = test_bot.heading
	    print("BOT NOW IN CELL:         {}".format(bot_position))
	    print("BOT HEADING IS :         {}".format(bot_heading))
	

	    time.sleep(0.02)

	    # Take new sensor measurements
	    sensor_measurements = test_bot.take_measurements()
	    # Create a new cell to store information.
	    new_cell = CELL(bot_position, open_dir = sensor_measurements)
	    # Append to current test_path
	    test_path.append_cell(new_cell)
	    test_path.print_path()
	    print("==========================\n")
	    if iter_cnt == 10:
	        break
	test_path.mark_map_end(bot_position, test_bot.heading)

except KeyboardInterrupt:
        stop()




