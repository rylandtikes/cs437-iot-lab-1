from time import sleep
import picar_4wd as fc

speed = 10

def main():
    turns = 0
    while turns < 9:
        scan_list = fc.scan_step(37)
        if not scan_list:
            continue
        scan_focus = scan_list[1:6]

        if scan_focus != [2,2,2,2] and len(scan_focus) > 4:
            fc.backward(speed)
            sleep(0.3)
            fc.turn_left(speed)
            sleep(0.2)
            turns += 1
        else:
            fc.forward(speed)
            sleep(0.3)
            turns += 1
    
    fc.stop()

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
