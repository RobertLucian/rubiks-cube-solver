FROM resin/rpi-raspbian:stretch
WORKDIR /solver

# RUN [ "cross-build-start" ]

RUN apt-get update -qq && \
    apt-get install libgtk2.0-dev libgtk-3-dev -y --no-install-recommends && \
    apt-get install python3 python3-dev python3-pip libraspberrypi-bin wiringpi -y --no-install-recommends \
    libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libatlas-base-dev gfortran \
    openexr libilmbase12 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libqtgui4 libqt4-test \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

RUN usermod -aG video root

# RUN [ "cross-build-end" ]

RUN pip3 install setuptools wheel
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY *.py ./

ENTRYPOINT ["tini", "-v", "--"]
CMD ["/usr/bin/python3", "main.py"]