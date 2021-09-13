#!/usr/bin/env python
"""
Test case for map
"""

import numpy as np
import sys
import copy

np.set_printoptions(threshold=sys.maxsize)

import matplotlib.pyplot as plt


__author__ = "Charles Stolz"
__email__ = "cstolz2@illinois.edu"
__status__ = "test case simulating sensors reading and creating a map"

# Size of 2D Numpy Array
NP_ARRAY_SIZE = 180

THRESHOLD = 10

SERVO_STEP = 10


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
    for sensor_readings in [
        sensor_readings_1,
        sensor_readings_2,
        sensor_readings_3,
        sensor_readings_4,
        sensor_readings_5,
        sensor_readings_6,
        sensor_readings_7,
        sensor_readings_8,
        sensor_readings_9,
        sensor_readings_10,
        sensor_readings_11,
    ]:
        numpy_array_map = create_map(sensor_readings)
        below_threshold_sensor_readings = filter_below_threshold(sensor_readings)

        x_min, x_max = -90, 90
        y_min, y_max = 0, 180
        extent = [x_min, x_max, y_min, y_max]
        # matplotlib before 1s added
        plt.title("Numpy Array Map before addings 1s")
        plt.imshow(numpy_array_map, interpolation="none", extent=extent, origin="lower")
        plt.show()

        # matplot lib after 1s added
        numpy_array_ones_added = add_ones(
            below_threshold_sensor_readings, numpy_array_map
        )

        plt.title("Numpy Array Map After addings 1s")
        plt.imshow(
            numpy_array_ones_added, interpolation="none", extent=extent, origin="lower"
        )
        plt.show()


if __name__ == "__main__":
    ## Tests from sensor
    sensor_readings_1 = [
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

    # step 16
    sensor_readings_2 = [
        {"angle": -90, "distance": -2},
        {"angle": -74, "distance": 6.74},
        {"angle": -58, "distance": 92.42},
        {"angle": -42, "distance": 47.79},
        {"angle": -26, "distance": 46.45},
        {"angle": -10, "distance": 47.93},
        {"angle": 6, "distance": 85.1},
        {"angle": 22, "distance": 83.47},
        {"angle": 38, "distance": 44.47},
        {"angle": 54, "distance": 43.5},
        {"angle": 70, "distance": 43.5},
        {"angle": 86, "distance": 44.79},
    ]

    # step 5
    sensor_readings_3 = [
        {"angle": -90, "distance": -2},
        {"angle": -85, "distance": 6.72},
        {"angle": -80, "distance": 6.68},
        {"angle": -75, "distance": 92.21},
        {"angle": -70, "distance": 92.1},
        {"angle": -65, "distance": 92.72},
        {"angle": -60, "distance": 92.86},
        {"angle": -55, "distance": 93.92},
        {"angle": -50, "distance": 99.96},
        {"angle": -45, "distance": 100.14},
        {"angle": -40, "distance": 103.36},
        {"angle": -35, "distance": 99.41},
        {"angle": -30, "distance": 98.88},
        {"angle": -25, "distance": 44.63},
        {"angle": -20, "distance": 42.25},
        {"angle": -15, "distance": 43.3},
        {"angle": -10, "distance": 43.81},
        {"angle": -5, "distance": 41.95},
        {"angle": 0, "distance": 42.01},
        {"angle": 5, "distance": 41.96},
        {"angle": 10, "distance": 42.0},
        {"angle": 15, "distance": 41.96},
        {"angle": 20, "distance": 41.8},
        {"angle": 25, "distance": 42.31},
        {"angle": 30, "distance": 43.73},
        {"angle": 35, "distance": 43.0},
        {"angle": 40, "distance": 43.03},
        {"angle": 45, "distance": 43.45},
        {"angle": 50, "distance": 118.95},
        {"angle": 55, "distance": 118.49},
        {"angle": 60, "distance": 119.58},
        {"angle": 65, "distance": -2},
        {"angle": 70, "distance": -2},
        {"angle": 75, "distance": -2},
        {"angle": 80, "distance": -2},
        {"angle": 85, "distance": -2},
    ]

    # step 5
    sensor_readings_4 = [
        {"angle": -90, "distance": -2},
        {"angle": -85, "distance": 6.98},
        {"angle": -80, "distance": 6.91},
        {"angle": -75, "distance": 92.11},
        {"angle": -70, "distance": 92.31},
        {"angle": -65, "distance": 92.67},
        {"angle": -60, "distance": 55.35},
        {"angle": -55, "distance": 93.98},
        {"angle": -50, "distance": 99.85},
        {"angle": -45, "distance": 100.43},
        {"angle": -40, "distance": 103.39},
        {"angle": -35, "distance": 99.2},
        {"angle": -30, "distance": 98.82},
        {"angle": -25, "distance": 44.81},
        {"angle": -20, "distance": 42.95},
        {"angle": -15, "distance": 43.25},
        {"angle": -10, "distance": 43.69},
        {"angle": -5, "distance": 41.81},
        {"angle": 0, "distance": 41.72},
        {"angle": 5, "distance": 42.53},
        {"angle": 10, "distance": 42.11},
        {"angle": 15, "distance": 42.31},
        {"angle": 20, "distance": 41.74},
        {"angle": 25, "distance": 42.31},
        {"angle": 30, "distance": 43.34},
        {"angle": 35, "distance": 42.95},
        {"angle": 40, "distance": 43.33},
        {"angle": 45, "distance": 44.03},
        {"angle": 50, "distance": 118.66},
        {"angle": 55, "distance": 118.2},
        {"angle": 60, "distance": 119.45},
        {"angle": 65, "distance": -2},
        {"angle": 70, "distance": -2},
        {"angle": 75, "distance": -2},
        {"angle": 80, "distance": -2},
        {"angle": 85, "distance": -2},
    ]

    # step 10
    sensor_readings_5 = [
        {"angle": -90, "distance": -2},
        {"angle": -80, "distance": 6.78},
        {"angle": -70, "distance": 92.09},
        {"angle": -60, "distance": 92.37},
        {"angle": -50, "distance": 93.54},
        {"angle": -40, "distance": 100.22},
        {"angle": -30, "distance": 99.25},
        {"angle": -20, "distance": 45.04},
        {"angle": -10, "distance": 43.7},
        {"angle": 0, "distance": 41.8},
        {"angle": 10, "distance": 42.29},
        {"angle": 20, "distance": 42.23},
        {"angle": 30, "distance": 42.32},
        {"angle": 40, "distance": 43.37},
        {"angle": 50, "distance": 44.13},
        {"angle": 60, "distance": 118.77},
        {"angle": 70, "distance": -2},
        {"angle": 80, "distance": -2},
    ]
    sensor_readings_6 = [
        {"angle": -90, "distance": 90.21},
        {"angle": -80, "distance": 6.67},
        {"angle": -70, "distance": 103.83},
        {"angle": -60, "distance": 104.2},
        {"angle": -50, "distance": 104.74},
        {"angle": -40, "distance": 106.19},
        {"angle": -30, "distance": -2},
        {"angle": -20, "distance": 121.63},
        {"angle": -10, "distance": 118.88},
        {"angle": 0, "distance": 117.93},
        {"angle": 10, "distance": 117.97},
        {"angle": 20, "distance": 117.52},
        {"angle": 30, "distance": 117.82},
        {"angle": 40, "distance": 118.44},
        {"angle": 50, "distance": 119.48},
        {"angle": 60, "distance": 93.89},
        {"angle": 70, "distance": 91.75},
        {"angle": 80, "distance": 90.55},
    ]
    sensor_readings_7 = [
        {"angle": -90, "distance": 90.64},
        {"angle": -80, "distance": 6.66},
        {"angle": -70, "distance": 103.61},
        {"angle": -60, "distance": 104.08},
        {"angle": -50, "distance": 104.63},
        {"angle": -40, "distance": 106.11},
        {"angle": -30, "distance": 109.12},
        {"angle": -20, "distance": 111.55},
        {"angle": -10, "distance": 7.81},
        {"angle": 0, "distance": 7.06},
        {"angle": 10, "distance": 8.01},
        {"angle": 20, "distance": 7.83},
        {"angle": 30, "distance": 7.1},
        {"angle": 40, "distance": 8.86},
        {"angle": 50, "distance": 6.86},
        {"angle": 60, "distance": 93.65},
        {"angle": 70, "distance": 90.96},
        {"angle": 80, "distance": 90.8},
    ]
    sensor_readings_8 = [
        {"angle": -90, "distance": 96.86},
        {"angle": -80, "distance": 93.59},
        {"angle": -70, "distance": 98.16},
        {"angle": -60, "distance": 96.8},
        {"angle": -50, "distance": 98.61},
        {"angle": -40, "distance": 105.19},
        {"angle": -30, "distance": -2},
        {"angle": -20, "distance": 38.29},
        {"angle": -10, "distance": 36.77},
        {"angle": 0, "distance": 36.28},
        {"angle": 10, "distance": 36.4},
        {"angle": 20, "distance": 36.75},
        {"angle": 30, "distance": 37.67},
        {"angle": 40, "distance": 38.86},
        {"angle": 50, "distance": 41.16},
        {"angle": 60, "distance": 122.61},
        {"angle": 70, "distance": 98.82},
        {"angle": 80, "distance": 97.4},
    ]

    sensor_readings_9 = [
        {"angle": -90, "distance": 97.02},
        {"angle": -80, "distance": 93.64},
        {"angle": -70, "distance": 94.28},
        {"angle": -60, "distance": 92.14},
        {"angle": -50, "distance": 97.59},
        {"angle": -40, "distance": 105.29},
        {"angle": -30, "distance": -2},
        {"angle": -20, "distance": -2},
        {"angle": -10, "distance": -2},
        {"angle": 0, "distance": -2},
        {"angle": 10, "distance": -2},
        {"angle": 20, "distance": -2},
        {"angle": 30, "distance": -2},
        {"angle": 40, "distance": -2},
        {"angle": 50, "distance": -2},
        {"angle": 60, "distance": 123.52},
        {"angle": 70, "distance": 99.25},
        {"angle": 80, "distance": 97.48},
    ]
    sensor_readings_10 = [
        {"angle": -90, "distance": 97.08},
        {"angle": -80, "distance": 97.11},
        {"angle": -70, "distance": 97.06},
        {"angle": -60, "distance": 97.04},
        {"angle": -50, "distance": 97.46},
        {"angle": -40, "distance": 98.13},
        {"angle": -30, "distance": 122.81},
        {"angle": 50, "distance": 123.46},
        {"angle": 60, "distance": 123.12},
        {"angle": 70, "distance": 122.67},
        {"angle": 80, "distance": 99.46},
    ]

    sensor_readings_11 = [
        {"angle": -90, "distance": 97.06},
        {"angle": -80, "distance": 97.16},
        {"angle": -70, "distance": 97.66},
        {"angle": -60, "distance": 99.91},
        {"angle": -50, "distance": 123.34},
        {"angle": -40, "distance": -2},
        {"angle": -30, "distance": -2},
        {"angle": -20, "distance": -2},
        {"angle": -10, "distance": -2},
        {"angle": 0, "distance": -2},
        {"angle": 10, "distance": -2},
        {"angle": 20, "distance": -2},
        {"angle": 30, "distance": -2},
        {"angle": 40, "distance": -2},
        {"angle": 50, "distance": 123.34},
        {"angle": 60, "distance": 123.35},
        {"angle": 70, "distance": 123.28},
        {"angle": 80, "distance": 122.81},
    ]
    main()
