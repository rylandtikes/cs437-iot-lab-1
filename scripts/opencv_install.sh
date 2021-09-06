#!/bin/bash
# Install opencv and all dependant libraries on raspberry pi

sudo apt-get install libhdf5-dev -y 
sudo apt-get install libhdf5-serial-dev -y 
sudo apt-get install libatlas-base-dev -y 
sudo apt-get install libjasper-dev -y 
sudo apt-get install libqtgui4 -y 
sudo apt-get install libqt4-test -y
pip3 install opencv-python
pip3 install -U numpy
pip3 install matplotlib
echo -e "testing opencv library available"
python3 -c "import cv2"
echo -e "testing numpy library available"
python3 -c "import numpy"
echo -e "testing matplotlib library available"
python3 -c "import matplotlib"
