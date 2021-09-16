#!/usr/bin/env python
"""
Expands on the map_cars_environment script and adds routing capabilities using A* for pathfinding.
"""

import numpy as np
import sys
import copy
from picar_4wd.pwm import PWM
from picar_4wd.filedb import FileDB
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time
import matplotlib.pyplot as plt
import picar_4wd as fc
from map_cars_environment import *

np.set_printoptions(threshold=sys.maxsize)

# Size of 2D Numpy Array
NP_ARRAY_SIZE = 180

# If below the threshold connect the points
THRESHOLD = 10

SERVO_STEP = 10

# Maximum number of distance trials when -2 is returned
MAX_DISTANCE_READINGS = 3

# Config File:
config = FileDB()
ultrasonic_servo_offset = int(config.get("ultrasonic_servo_offset", default_value=0))

us = Ultrasonic(Pin("D8"), Pin("D9"))

servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

power_val = 50

def main():
    val = input("Press any key to start, press q to quit")

    while(val != 'q'):
        fc.forward(power_val)
        servo.set_angle(0)
        sensor_readings = []
        for i in range(0, 180, SERVO_STEP):
            angle = i - 90
            move_servo(angle)
            distance = get_distance()
            if distance < 180:
                sensor_readings.append({"angle": angle, "distance": distance})

        numpy_array_map = create_map(sensor_readings)
        below_threshold_sensor_readings = filter_below_threshold(sensor_readings)
        numpy_array_ones_added = add_ones(below_threshold_sensor_readings, numpy_array_map)
        servo.set_angle(0)

        print(numpy_array_ones_added)

        if not np.any(numpy_array_ones_added == 1):
            fc.forward(power_val)
        else:
            fc.turn_right(power_val)


if __name__ == "__main__":
    main()
