import cv2
import logging
import datetime
import time
import numpy as np
import picar_4wd as fc
from PIL import Image
from traffic_objects import *
from tflite_runtime.interpreter import load_delegate
from tflite_runtime.interpreter import Interpreter
_SHOW_IMAGE = False

class ObjectsOnRoadProcessor(object):
    """
    This class 1) detects what objects (namely traffic signs and people) are on the road
    and controls car speed accordingly. Source for the trained model:
    https://github.com/dctian/DeepPiCar/tree/master/models/object_detection/data/model_result
    """

    def __init__(self,
                 car=None,
                 speed_limit=1,
                 model='/home/pi/IoT/Lab 1/road_signs_quantized_edgetpu.tflite',
                 label='/home/pi/IoT/Lab 1/road_sign_labels.txt',
                 width=640,
                 height=480):
        # model: Using model compiled for Edge TPU.

        logging.info('Creating a ObjectsOnRoadProcessor...')
        self.width = width
        self.height = height

        # initialize car
        self.car = car
        self.speed_limit = speed_limit
        self.speed = speed_limit

        # initialize TensorFlow models
        with open(label, 'r') as f:
            pairs = (l.strip().split(maxsplit=1) for l in f.readlines())
            self.labels = dict((int(k), v) for k, v in pairs)

        # initialized edge TPU Interpreter
        logging.info('Initialize Edge TPU with model %s...' % model)
        self.interpreter = Interpreter(model,
        experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        self.interpreter.allocate_tensors()
        _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']
        self.min_confidence = 0.45
        self.num_of_objects = 3
        logging.info('Initialize Edge TPU with model done.')

        # parameters for bounding boxes
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10, height - 10)
        self.fontScale = .5
        self.fontColor = (255, 255, 255)  # white
        self.boxColor = (0, 0, 255)  # RED
        self.boxLineWidth = 1
        self.lineType = 2
        self.annotate_text = ""
        self.annotate_text_time = time.time()
        self.time_to_show_prediction = 1.0  # ms

        # define the traffic objects
        self.traffic_objects = {0: GreenTrafficLight(),
                                1: Person(),
                                2: RedTrafficLight(),
                                3: SpeedLimit(2),
                                4: SpeedLimit(3),
                                5: StopSign()}

    def process_objects_on_road(self, frame):
        # Main entry point of the Road Object Handler
        logging.debug('Processing objects.................................')
        objects, final_frame = self.detect_objects(frame)
        self.control_car(objects)
        logging.debug('Processing objects END..............................')

        return final_frame

    def control_car(self, objects):
        logging.debug('Control car...')
        car_state = {"speed": self.speed_limit, "speed_limit": self.speed_limit}

        if len(objects) == 0:
            logging.debug('No objects detected, drive at speed limit of %s.' % self.speed_limit)

        contain_stop_sign = False
        for obj in objects:
            obj_label = self.labels[obj['class_id']]
            processor = self.traffic_objects[obj['class_id']]
            if processor.is_close_by(obj, self.height):
                processor.set_car_state(car_state)
            else:
                logging.debug("[%s] object detected, but it is too far, ignoring. " % obj_label)
            if obj_label == 'Stop':
                contain_stop_sign = True

        if not contain_stop_sign:
            self.traffic_objects[5].clear()

        self.resume_driving(car_state)

    def resume_driving(self, car_state):
        old_speed = self.speed
        self.speed_limit = car_state['speed_limit']
        self.speed = car_state['speed']

        if self.speed == 0:
            self.set_speed(0)
        else:
            self.set_speed(self.speed_limit)
        logging.debug('Current Speed = %d, New Speed = %d' % (old_speed, self.speed))

        if self.speed == 0:
            logging.debug('Full stop for 1 seconds')
            time.sleep(1)

    def set_speed(self, speed):
        # Use this setter, so we can test this class without a car attached
        self.speed = speed
        if self.car is not None:
            logging.debug("Setting car speed to %d" % speed)
            if speed == 0:
                self.car.wheels.forward(0)
            else:
                self.car.wheels.forward(speed)

    def set_input_tensor(self,interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def get_output_tensor(self,interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor

    def detect_with_image(self,interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(interpreter, 0)
        classes = self.get_output_tensor(interpreter, 1)
        scores = self.get_output_tensor(interpreter, 2)
        count = int(self.get_output_tensor(interpreter, 3))
        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results



    ############################
    # Frame processing steps
    ############################
    def detect_objects(self, frame):
        """ Uses the Edge TPU for inference. Bounding boxes are
        determined by four axis values of the output tensor.
        """
        logging.debug('Detecting objects...')

        start_ms = time.time()
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pre_img = Image.fromarray(frame_RGB)
        img_pil = pre_img.resize(
            (self.input_width, self.input_height), Image.ANTIALIAS)
        objects = self.detect_with_image(self.interpreter, img_pil,self.min_confidence)
        if objects:
            for obj in objects:
                height = (obj['bounding_box'][3]-obj['bounding_box'][1]) * self.height
                width = (obj['bounding_box'][2]- obj['bounding_box'][0]) * self.width
                logging.debug("%s, %.0f%% w=%.0f h=%.0f" % (self.labels[obj['class_id']], obj['score'] * 100, width, height))
                box = obj['bounding_box']
                coord_top_left = (int(box[1] * 640), int(box[2] * 480))
                coord_bottom_right = (int(box[3] * 640), int(box[0] * 480))
                cv2.rectangle(frame, coord_top_left, coord_bottom_right, self.boxColor, self.boxLineWidth)
                annotate_text = "%s %.0f%%" % (self.labels[obj['class_id']], obj['score'] * 100)
                coord_top_left = (coord_top_left[0], coord_top_left[1] + 30)
                cv2.putText(frame, annotate_text, coord_top_left, self.font, self.fontScale, self.boxColor, self.lineType)
        else:
            logging.debug('No object detected')

        elapsed_ms = time.time() - start_ms

        annotate_summary = "%.1f FPS" % (1.0/elapsed_ms)
        logging.debug(annotate_summary)
        cv2.putText(frame, annotate_summary, self.bottomLeftCornerOfText, self.font, self.fontScale, self.fontColor, self.lineType)

        return objects, frame


############################
# Utility Functions
############################
def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)


############################
# Test Functions
############################
def test_photo(file):
    object_processor = ObjectsOnRoadProcessor()
    frame = cv2.imread(file)
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Detected Objects', combo_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_stop_sign():
    # this simulates a car at stop sign
    object_processor = ObjectsOnRoadProcessor()
    frame = cv2.imread('/home/pi/IoT/Lab 1/data/objects/stop_sign.jpg')
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 1', combo_image)
    time.sleep(1)
    frame = cv2.imread('/home/pi/IoT/Lab 1/data/objects/stop_sign.jpg')
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 2', combo_image)
    time.sleep(2)
    frame = cv2.imread('/home/pi/IoT/Lab 1/data/objects/stop_sign.jpg')
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 3', combo_image)
    time.sleep(1)
    frame = cv2.imread('/home/pi/IoT/Lab 1/data/objects/green_light.jpg')
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 4', combo_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    
    # testing object recognition
    test_photo('/home/pi/IoT/Lab 1/data/objects/green_light.jpg')
    test_photo('/home/pi/IoT/Lab 1/data/objects/no_obj.jpg')

    # test stop sign, which carries state
    test_stop_sign()