#!/bin/bash

sudo apt-get update

# setup python3 pip + libraries required for Adafruit OLED display lib
sudo apt-get install -y python3-pip python3-pil python3-numpy

pip3 install adafruit-circuitpython-ssd1306  --break-system-packages


# to be able to use command, like 'i2cdetect -y 1'
sudo apt-get install -y i2c-tools

# networking libs to print current IP
pip3 install netifaces  --break-system-packages

# enable i2c
sudo sed -i 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/config.txt

# increase I2C bus speed to 1MHz
#sudo sed -i 's/# Uncomment this to enable infrared communication./dtparam=i2c_baudrate=1000000\n\n# Uncomment this to enable infrared communication./g' /boot/config.txt

sudo apt-get install -y git

cd /home/pi/
git clone https://github.com/symat/sztehlo-telescope.git

sudo cp /home/pi/sztehlo-telescope/pi/oled.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable oled.service


# install web server 
pip3 install Flask --break-system-packages

sleep 60

sudo reboot


