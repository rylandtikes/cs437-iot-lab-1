'''
This program contains the PiCar obstacle detection implementation.
The car will attempt to drive forward if an obstacle is not detected
by the ultrasonic sensor. Otherwise, the car will reverse and turn left
until the path is clear to move forward.
'''

from time import sleep
import picar_4wd as fc

speed = 10

def main():
    turns = 0
    while turns < 9:
        #set the scan distance to 37 centimeters
        scan_list = fc.scan_step(37)
        if not scan_list:
            continue
        scan_focus = scan_list[1:6]
        if scan_focus != [2,2,2,2,2] and len(scan_focus) > 4:
            fc.backward(speed)
            sleep(.3)
            fc.turn_left(speed)
            sleep(.2)
            turns += 1
        else:
            fc.forward(speed)
            sleep(.3)
            turns += 1
    fc.stop
if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
