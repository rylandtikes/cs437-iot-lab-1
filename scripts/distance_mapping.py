#!/usr/bin/env python
"""
Interpolates distance measurements between angle readings 
"""

from picar_4wd.pwm import PWM
from picar_4wd.filedb import FileDB
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time
import numpy as np

# Config File:
config = FileDB()
ultrasonic_servo_offset = int(config.get("ultrasonic_servo_offset", default_value=0))

# Initialize picar modules
us = Ultrasonic(Pin("D8"), Pin("D9"))
servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

#Initialize numpy array, distances dict, threshold dist 
area_map = np.zeros((100, 100))
car_position = (0, 0)
distances = {}

# This is arbitrary
thres = 10 

def test_servo(start, end):
    for angle in range(start, end + 10, 5):
        #print(f"testing servo at {angle}")
        servo.set_angle(angle)
        distance = get_distance()
        distances.update([(angle, distance)])

def get_distance():
    distance = us.get_distance()
    print(f"Distance is {distance}")
    return distance

def calculate_slope(x1, x2, y1, y2):
    slope = (y2 - y1) / (x2 - x1)
    return slope

def make_map():
    for k,v in distances.items():
        ang = k
        dist = v 
        print(ang, ": ", dist)
        if(dist < thres):
            area_map[0][ang-5] = 1
            area_map[0][ang-4] = 1
            area_map[0][ang-3] = 1
            area_map[0][ang-2] = 1
            area_map[0][ang-1] = 1
        else:
            area_map[0][ang-5] = 0
            area_map[0][ang-4] = 0
            area_map[0][ang-3] = 0
            area_map[0][ang-2] = 0
            area_map[0][ang-1] = 0
    # Just print the first 3 rows for simplicity        
    return print(area_map[0:3])

if __name__ == "__main__":
    #TODO: Add logic to call the make_map function each time the car moves
    #while(True):
    test_servo(-90, 85)
    make_map()
