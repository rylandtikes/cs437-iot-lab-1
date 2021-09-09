#!/usr/bin/env python
"""
Test case for mapping from Ultrasonic Sensor
"""

import numpy as np
import sys


np.set_printoptions(threshold=sys.maxsize)

import matplotlib.pyplot as plt


__author__ = "Charles Stolz"
__email__ = "cstolz2@illinois.edu"
__status__ = "test case simulating sensors reading and creating a map"

# Size of 2D Numpy Array
NP_ARRAY_SIZE = 180

# If below the threshold connect the points
THRESHOLD = 10


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
    for i in range(len(sensor_readings) - 1):
        print(sensor_readings[i])
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


def main():
    # Test data from actual sensor readings
    sensor_readings = [
        {"angle": -90, "distance": 91.19},
        {"angle": -85, "distance": 5.92},
        {"angle": -80, "distance": 6.84},
        {"angle": -75, "distance": 102.59},
        {"angle": -70, "distance": 102.56},
        {"angle": -65, "distance": 102.5},
        {"angle": -60, "distance": 45.43},
        {"angle": -55, "distance": 43.68},
        {"angle": -50, "distance": 43.51},
        {"angle": -45, "distance": 43.65},
        {"angle": -40, "distance": 44.45},
        {"angle": -35, "distance": 42.66},
        {"angle": -30, "distance": 43.97},
        {"angle": -25, "distance": 43.77},
        {"angle": -20, "distance": 43.67},
        {"angle": -15, "distance": 43.28},
        {"angle": -10, "distance": 45.42},
        {"angle": -5, "distance": 44.69},
        {"angle": 0, "distance": 48.51},
        {"angle": 5, "distance": 54.81},
        {"angle": 10, "distance": 127.66},
        {"angle": 15, "distance": 54.76},
        {"angle": 20, "distance": 53.97},
        {"angle": 25, "distance": 52.96},
        {"angle": 30, "distance": 53.12},
        {"angle": 35, "distance": 53.39},
        {"angle": 40, "distance": 53.1},
        {"angle": 45, "distance": 53.14},
        {"angle": 50, "distance": 53.04},
        {"angle": 55, "distance": 53.14},
        {"angle": 60, "distance": 53.54},
        {"angle": 65, "distance": 54.08},
        {"angle": 70, "distance": 55.08},
        {"angle": 75, "distance": 91.99},
        {"angle": 80, "distance": 91.78},
        {"angle": 85, "distance": 91.42},
    ]

    # Initial map without the ones between the points
    numpy_array_map = create_map(sensor_readings)

    # Will be used to create second numpy array with ones between the points
    below_threshold_sensor_readings = filter_below_threshold(sensor_readings)

    plt.title("Numpy Array Map before addings 1s")
    plt.imshow(
        numpy_array_map,
        interpolation="none",
    )
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    main()
