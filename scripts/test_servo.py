#!/usr/bin/env python
"""
Tests the servo library
"""

from picar_4wd.pwm import PWM
from picar_4wd.filedb import FileDB
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time

__author__ = "Charles Stolz"
__credits__ = ["sunfounder.com"]
__email__ = "cstolz2@illinois.edu"
__status__ = "test"

# Config File:
config = FileDB()
ultrasonic_servo_offset = int(config.get("ultrasonic_servo_offset", default_value=0))

us = Ultrasonic(Pin("D8"), Pin("D9"))


servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)


def test_servo(start, end):
    for i in range(start, end + 10, 10):
        print(f"testing servo at {i}")
        servo.set_angle(i)
        get_distance()
        time.sleep(2)


def get_distance():
    distance = us.get_distance()
    print(f"Distance is {distance}")
    return distance


if __name__ == "__main__":
    test_servo(-90, 90)
