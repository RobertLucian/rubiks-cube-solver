# Rubik's Cube Solver Robot
The software that solves the Rubik's Cube on a physical machine.
The detailed post on how this robot works can be found [here]().

An example of the robot scanning and then solving the Rubik's cube is shown in the next video.

[![](https://img.youtube.com/vi/GnsUHpGSF7Y/0.jpg)](https://www.youtube.com/watch?v=GnsUHpGSF7Y)

## Hardware

### Electronics

### Mechanics

## GUI App

### Overall Architecture

### Installing

Update the package manager:
```bash
sudo apt-get update
```

Numpy/Sklearn Dependencies:
```bash
sudo apt-get install gfortran libatlas-base-dev libopenblas-dev liblapack-dev
```

Dependencies for Pillow:
```bash
sudo apt-get install libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5 -y
```

Dependencies for muodov/kociemba library:
```bash
sudo apt-get install libffi-dev python-dev python3-dev
```

Dependencies for OpenCV:
```bash
sudo apt-get install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test libwebp6 -y
sudo apt-get install libatlas3-base libsz2 libharfbuzz0b libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtcore4 -y
```

Then, after having installed the dependencies, go on and install the actual libraries:
```bash
virtualenv -p python3 .venv # this has been tested against 3.5
source .venv/bin/activate
pip install -r requirements.txt --index-url https://piwheels.org/simple --extra-index-url https://pypi.org/simple
```

### Usage

To run this, execute
```bash
python main.py
```

This launches a GUI app, so be sure you've got an X11 client running on your computer if you're running this headless.