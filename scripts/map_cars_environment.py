#!/usr/bin/env python
"""
Test case for map
"""

import numpy as np
import sys
import math
import copy
from picar_4wd.pwm import PWM
from picar_4wd.filedb import FileDB
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time


np.set_printoptions(threshold=sys.maxsize)

import matplotlib.pyplot as plt


__author__ = "Charles Stolz"
__email__ = "cstolz2@illinois.edu"
__status__ = "test case simulating sensors reading and creating a map"

# Size of 2D Numpy Array
NP_ARRAY_SIZE = 180

# If below the threshold connect the points
THRESHOLD = 10

SERVO_STEP = 10

# Config File:
config = FileDB()
ultrasonic_servo_offset = int(config.get("ultrasonic_servo_offset", default_value=0))

us = Ultrasonic(Pin("D8"), Pin("D9"))


servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)


def move_servo(angle):
    print(f"testing servo at {angle}")
    servo.set_angle(angle)


def get_distance():
    distance = us.get_distance()
    print(f"Distance is {distance}")
    return distance


def create_map(sensor_readings: list) -> list:
    """
    add 1s from the initial readings
    """
    x = NP_ARRAY_SIZE
    y = NP_ARRAY_SIZE
    a = np.zeros(shape=(x, y))
    for sensor_reading in sensor_readings:
        angle = int(sensor_reading["angle"])
        distance = int(sensor_reading["distance"])
        a[distance][angle + 90] = 1
    return a


def calculate_slope(x1, x2, y1, y2):
    slope = (y2 - y1) / (x2 - x1)
    return slope


def filter_below_threshold(sensor_readings: list) -> list:
    below_threshold = []
    for i in range(0, len(sensor_readings) - 1, 2):
        # print(sensor_readings[i])
        x1 = sensor_readings[i]["angle"]
        y1 = sensor_readings[i]["distance"]
        x2 = sensor_readings[i + 1]["angle"]
        y2 = sensor_readings[i + 1]["distance"]
        slope = calculate_slope(x1, x2, y1, y2)
        if slope < THRESHOLD:
            print(sensor_readings[i])
            print(sensor_readings[i + 1])
            print(f"{y2} - {y1} / {x2} - {x1}")
            print(f"add a 1 slope is {slope}")
            print(slope)
            below_threshold.append(sensor_readings[i])
            below_threshold.append(sensor_readings[i + 1])
    return below_threshold


def add_ones(sensor_readings: list, numpy_array_map: list) -> list:
    """
    add 1s from the initial readings
    """
    numpy_array_ones_added = copy.deepcopy(numpy_array_map)
    for i in range(len(sensor_readings) - 1):
        angle1 = int(sensor_readings[i]["angle"])
        distance1 = int(sensor_readings[i]["distance"])
        angle2 = int(sensor_readings[i + 1]["angle"])
        distance2 = int(sensor_readings[i + 1]["distance"])
        print(angle1, angle2)
        numpy_array_ones_added[distance1][angle1 + 90 : angle2 + 90] = 1
        numpy_array_ones_added[distance2][angle1 + 90 : angle2 + 90] = 1
    return numpy_array_ones_added


def main():

    sensor_readings = []
    for i in range(0, 180, SERVO_STEP):
        angle = i - 90
        move_servo(angle)
        distance = get_distance()
        sensor_readings.append({"angle": angle, "distance": distance})
        time.sleep(1)

    numpy_array_map = create_map(sensor_readings)
    below_threshold_sensor_readings = filter_below_threshold(sensor_readings)

    print(sensor_readings)

    plt.title("Numpy Array Map before addings 1s")
    plt.imshow(
        numpy_array_map,
        interpolation="none",
    )
    plt.gca().invert_yaxis()
    plt.show()

    numpy_array_ones_added = add_ones(below_threshold_sensor_readings, numpy_array_map)

    plt.title("Numpy Array Map After addings 1s")
    plt.imshow(
        numpy_array_ones_added,
        interpolation="none",
    )
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    main()
