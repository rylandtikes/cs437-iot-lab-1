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
thres = 25

def test_servo(start, end):
    for angle in range(start, end + 10, 5):
        print(f"testing servo at {angle}")
        servo.set_angle(angle)
        distance = get_distance()
        distances.update([(angle, distance)])

def get_distance():
    distance = us.get_distance()
    #print(f"Distance is {distance}")
    return distance

def interpolate(v1,v2,t):
    t = (t - v1) / (v2 - v1)
    return t

def make_map():
    for i in distances:
        dist = distances[i]
        print("distance: ", dist)
        if(dist > thres):
            area_map[i] = 1
        else: 
            area_map[i] = 0
    return print(area_map)

if __name__ == "__main__":
    test_servo(-90, 85)
    make_map()
