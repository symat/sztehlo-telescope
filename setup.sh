#!/bin/bash

sudo apt-get update

# setup python3 pip + libraries required for Adafruit OLED display lib
sudo apt-get install -y python3-pip python3-pil python3-numpy

pip3 install adafruit-circuitpython-ssd1306

# to be able to use command, like 'i2cdetect -y 1'
sudo apt-get install -y i2c-tools

# networking libs to print current IP
pip3 install netifaces

# enable i2c
sudo sed -i 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/config.txt

# increase I2C bus speed to 1MHz
#sudo sed -i 's/# Uncomment this to enable infrared communication./dtparam=i2c_baudrate=1000000\n\n# Uncomment this to enable infrared communication./g' /boot/config.txt

