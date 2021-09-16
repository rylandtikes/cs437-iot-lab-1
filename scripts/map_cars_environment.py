#!/usr/bin/env python
"""
Measures distance from Ultrasonic sensor then builds a 2D map. Plots the map to the
screen. In order to display plot on raspberry pi execute in shell. Using VNC 
viewer with the PI you can see the plots on the screen.
export DISPLAY=:0.0
"""

import numpy as np
import copy
from picar_4wd.pwm import PWM
from picar_4wd.filedb import FileDB
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time
import matplotlib.pyplot as plt
import picar_4wd as fc


# Size of 2D Numpy Array
NP_ARRAY_SIZE = 180

# If below the threshold connect the coordinates
THRESHOLD = 1

SERVO_STEP = 10

# Maximum number of distance trials when -2 is returned
MAX_DISTANCE_READINGS = 3

# Config File:
config = FileDB()
ultrasonic_servo_offset = int(config.get("ultrasonic_servo_offset", default_value=0))

us = Ultrasonic(Pin("D8"), Pin("D9"))


servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)


def move_servo(angle):
    servo.set_angle(angle)
    time.sleep(0.3)


def get_distance():
    number_distance_readings = 0
    while number_distance_readings < MAX_DISTANCE_READINGS:
        distance = us.get_distance()
        if distance != -2:
            break
        number_distance_readings += 1
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
    for i in range(0, len(sensor_readings) - 1):
        reading1 = sensor_readings[i]
        reading2 = sensor_readings[i + 1]
        x1 = reading1["angle"]
        y1 = reading1["distance"]
        x2 = reading2["angle"]
        y2 = reading2["distance"]
        slope = calculate_slope(x1, x2, y1, y2)
        if abs(slope) < THRESHOLD:
            if reading1 not in below_threshold:
                below_threshold.append(reading1)
            below_threshold.append(reading2)
    return below_threshold


def add_ones(sensor_readings: list, numpy_array_map: list) -> list:
    """
    add 1s from the initial readings
    """
    numpy_array_ones_added = copy.deepcopy(numpy_array_map)
    for i in range(0, len(sensor_readings) - 1):
        angle1 = int(sensor_readings[i]["angle"])
        distance1 = int(sensor_readings[i]["distance"])
        angle2 = int(sensor_readings[i + 1]["angle"])
        distance2 = int(sensor_readings[i + 1]["distance"])
        numpy_array_ones_added[distance1][angle1 + 90 : angle2 + 90] = 1
        numpy_array_ones_added[distance2][angle1 + 90 : angle2 + 90] = 1
    return numpy_array_ones_added


def get_sensor_readings():
    sensor_readings = []
    for i in range(0, 180, SERVO_STEP):
        angle = i - 90
        move_servo(angle)
        distance = get_distance()
        if distance == -2:
            distance = 179
        if distance > 0 and distance < 180:
            sensor_readings.append({"angle": angle, "distance": distance})
    return sensor_readings


def create_matplot_lib_map(numpy_array_map, numpy_array_ones_added):
    x_min, x_max = -90, 90
    y_min, y_max = 0, 180
    extent = [x_min, x_max, y_min, y_max]

    # matplotlib before 1s added
    plt.title("Numpy Array Map before addings 1s")
    plt.imshow(numpy_array_map, interpolation="none", extent=extent, origin="lower")
    plt.show()

    # matplot lib after 1s added
    plt.title("Numpy Array Map After addings 1s")
    plt.imshow(
        numpy_array_ones_added, interpolation="none", extent=extent, origin="lower"
    )
    plt.show()


def main():
    servo.set_angle(0)
    sensor_readings = get_sensor_readings()
    print(sensor_readings)
    numpy_array_map = create_map(sensor_readings)
    below_threshold_sensor_readings = filter_below_threshold(sensor_readings)
    numpy_array_ones_added = add_ones(below_threshold_sensor_readings, numpy_array_map)
    create_matplot_lib_map(numpy_array_map, numpy_array_ones_added)
    servo.set_angle(0)


if __name__ == "__main__":
    main()
