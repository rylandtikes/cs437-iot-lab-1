import logging
import picar_4wd as fc
import cv2
import datetime
from objects_on_road_processor import ObjectsOnRoadProcessor

_SHOW_IMAGE = True


class DeepPiCar(object):

    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 640
    __SCREEN_HEIGHT = 480

    def __init__(self):
        """ Initialize camera and wheels. Reference for car boilerplate: 
        https://github.com/dctian/DeepPiCar"""
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)
        self.speed = 0
        self.wheels = fc
        self.traffic_sign_processor = ObjectsOnRoadProcessor(self)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        datestr = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.video_orig = self.create_video_recorder('IoT/car_video%s.avi' % datestr)
        self.video_lane = self.create_video_recorder('IoT/car_video_lane%s.avi' % datestr)
        self.video_objs = self.create_video_recorder('IoT/car_video_objs%s.avi' % datestr)

        logging.info('Created a DeepPiCar')

    def create_video_recorder(self, path):
        return cv2.VideoWriter(path, self.fourcc, 15.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def __enter__(self):
        """ Entering a with statement """
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)

        self.cleanup()

    def cleanup(self):
        """ Reset the hardware"""
        logging.info('Stopping the car, resetting hardware.')
        self.wheels.stop()
        self.camera.release()
        self.video_orig.release()
        self.video_lane.release()
        self.video_objs.release()
        cv2.destroyAllWindows()

    def drive(self, speed=__INITIAL_SPEED):
        """ Main entry point of the car, and put it in drive mode
        Keyword arguments:
        speed -- controls the car's four motors
        """

        logging.info('Starting to drive at speed %s...' % speed)
        self.wheels.forward(speed)
        i = 0
        while self.camera.isOpened():
            _, image_lane = self.camera.read()
            image_objs = image_lane.copy()
            i += 1
            image_objs = self.process_objects_on_road(image_objs)
            self.video_objs.write(image_objs)
            show_image('Detected Objects', image_objs)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break

    def process_objects_on_road(self, image):
        image = self.traffic_sign_processor.process_objects_on_road(image)
        return image


############################
# Utility Functions
############################
def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)


def main():
    with DeepPiCar() as car:
        car.drive(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    main()
