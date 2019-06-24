# Rubik's Cube Solver Robot
The software that solves the Rubik's Cube on a physical machine.

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
sudo apt-get install libffi-dev
```

Dependencies for OpenCV:
```bash
sudo apt-get install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test -y
```

Then, after having installed the dependencies, go on and install the actual libraries:
```bash
virtualenv -p python3 .venv # this has been tested against 3.5
source .venv/bin/activate
pip install -r requirements.txt --index-url https://piwheels.org/simple --extra-index-url https://pypi.org/simple
```

### Usage