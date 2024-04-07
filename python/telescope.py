import board
import busio
import adafruit_ssd1306
import digitalio
import time
import netifaces
import ipaddress
import socket
import os
import requests
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import threading
import subprocess
import re
import sys
from gpiozero import OutputDevice, InputDevice, MCP3008

HOST_REGEXP = r"\w+-(\d+)"
BORDER = 2
PI_BOARD_HOST = "http://gumicsizma.duckdns.org:5000"
LINE_BUFFER_LENGTH = 10

JOYSTICK_READ_TIME = 0.8  # time between two joystick state read
MOTOR_SLEEP_TIME = 0.005  # time to sleep between two motor steps
SLOW_STEPS = 3            # number of steps in slow mode (when joystick is not in the end)
                          # 3 steps = (200/360/51)*3 ~= 0.106 degree

reset_pin = digitalio.DigitalInOut(board.D4)
reset_pin.switch_to_output()

def reset_oled():
   reset_pin.value = False
   time.sleep(0.2)
   reset_pin.value = True
   time.sleep(0.2)

class TelescopeMotor:
    def __init__(self, red_pin, blue_pin, green_pin, black_pin):
        
        self.devices = [OutputDevice(red_pin),    # red   (1st coil, +)
                        OutputDevice(blue_pin),   # blue  (1st coil, -)
                        OutputDevice(green_pin),  # green (2nd coil, +)
                        OutputDevice(black_pin)]  # black (2nd coil, -)
        self.current_phase = 0
        self.phases = [[1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1]]
        for i in range(4):
            self.devices[i].off()
        

    def update_output(self):
        for i in range(4):
            if self.devices[i].value != self.phases[self.current_phase][i]:
                self.devices[i].toggle()

    def forward(self):
        self.current_phase = (self.current_phase + 1) % 4;
        self.update_output()   

    def backward(self):
        self.current_phase = (self.current_phase - 1) % 4;
        self.update_output()   


class TelescopeOled:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

        # Clear display.
        self.oled.fill(0)
        self.oled.show()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a white background
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)

        # Draw a smaller inner rectangle
        self.draw.rectangle(
            (BORDER, BORDER, self.oled.width - BORDER - 1, self.oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )

        self.updateHeader()

        # Load default font.
        self.font = ImageFont.load_default()
        (self.font_width, self.font_height) = self.font.getsize("H")

        self.number_of_rows = (64 - 4 * BORDER) // self.font_height
        self.start_x = 2 * BORDER
        self.start_y = 2 * BORDER



    def getNumberOfLinesAllowed(self):
        return int(self.number_of_rows - len(self.header))
    
    def updateHeader(self):
        self.header = [
            "HOST: " + socket.gethostname(),
            "IP: " + get_ip_text()
        ]

    def redraw(self, lines):
        self.draw.rectangle(
            (BORDER, BORDER, self.oled.width - BORDER - 1, self.oled.height - BORDER - 1),
            outline=0,
            fill=0,)
        self.draw.rectangle(
            (BORDER, BORDER, self.oled.width - BORDER - 1, self.start_y + len(self.header) * self.font_height),
            outline=255,
            fill=255,)
        y = self.start_y
        for line in self.header:
            self.draw.text((self.start_x, y), line, font=self.font, fill=0)
            y += self.font_height
        for line in lines:
            self.draw.text((self.start_x, y), line, font=self.font, fill=255)
            y += self.font_height

        # Display image
        self.oled.image(self.image)
        self.oled.show()



def get_local_non_loopback_ipv4_addresses():
    for interface in netifaces.interfaces():
        # Not all interfaces have an IPv4 address:
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            # Some interfaces have multiple IPv4 addresses:
            for address_info in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address_object = ipaddress.IPv4Address(str(address_info['addr']))
                if not address_object.is_loopback:
                    yield address_info['addr']

def get_ip_text():
    return ','.join(list(get_local_non_loopback_ipv4_addresses()))

def get_hostname_postfix():
    result = re.search(HOST_REGEXP, socket.gethostname())
    if len(result.groups()) > 0:
        return int(result.group(1))
    return 0



lines = deque(["", "Hello!"], maxlen=LINE_BUFFER_LENGTH)
telescopeOled = None

def check_oled():
    global telescopeOled
    last_warn_minute = 0
    while True:
        try:
            completedProc = subprocess.run(['i2cget', '-y', '1', '0x3c'],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)
            if completedProc.returncode == 0 and telescopeOled == None:
                reset_oled()
                print("I2C device found, will start to display")
                telescopeOled = TelescopeOled()
            if completedProc.returncode != 0:
                if telescopeOled != None:
                    print("unable to communicate on I2C, will stop displaying")
                    telescopeOled = None
                else:
                    current_minute = time.time_ns() // 60000000000 
                    if current_minute != last_warn_minute:
                        print("still unable to communicate on I2C, waiting for oled display")
                        last_warn_minute = current_minute
                reset_oled()
        except Exception as e:
            print(str(e))
        time.sleep(5)

checking_thread = threading.Thread(target=check_oled)
checking_thread.daemon = True

print("Starting oled checking thread")
checking_thread.start()


def redraw_oled():
    last_lines = list()
    last_change_time = 0
    changed = False
    min_wait_ns = 100000   # 0.1 sec
    while True:
        try:
            if telescopeOled != None:
                current_lines = list(lines)[-telescopeOled.getNumberOfLinesAllowed():]
                if last_lines != current_lines:
                    last_lines = current_lines
                    last_change_time = time.time_ns()
                    changed = True
                else: 
                    time.sleep(0.02)

                if changed and time.time_ns() - last_change_time > min_wait_ns: 
                    changed = False
                    telescopeOled.redraw(last_lines)

            else:
                time.sleep(0.3)
        except Exception as e:
            print(str(e))
            time.sleep(1)

        

redraw_thread = threading.Thread(target=redraw_oled)
redraw_thread.daemon = True
print("Starting oled refresh thread")
redraw_thread.start()


def motor_control():
    motor_x = TelescopeMotor(14, 15, 18, 23)
    motor_y = TelescopeMotor(24, 25, 7, 12)
    joystick_x = MCP3008(channel=6)
    joystick_y = MCP3008(channel=7)

    while True:
        try:
            x = joystick_x.value
            y = joystick_y.value
            fast_steps = int(JOYSTICK_READ_TIME / MOTOR_SLEEP_TIME)
            for i in range(fast_steps): 
                if x < 0.1 or (x < 0.4 and i < SLOW_STEPS):
                    motor_x.backward()
                if x > 0.9 or (x > 0.6 and i < SLOW_STEPS):
                    motor_x.forward()
                if y < 0.1 or (y < 0.4 and i < SLOW_STEPS):
                    motor_y.backward()
                if y > 0.9 or (y > 0.6 and i < SLOW_STEPS):
                    motor_y.forward()
                time.sleep(MOTOR_SLEEP_TIME)
        except Exception as e:
            print(str(e))
            time.sleep(1)

motor_control_thread = threading.Thread(target=motor_control)
motor_control_thread.daemon = True
print("Starting motor control thread")
motor_control_thread.start()



def sendMessageToBoard(hostId, ip, message):
    requests.post(PI_BOARD_HOST+'/messages/'+str(hostId), json={"ip": ip, "message": message})



hostId = get_hostname_postfix()
ip = get_ip_text()
for line in lines:
    sendMessageToBoard(hostId, ip, line)

FIFO = '/home/pi/oled'
if not os.path.exists(FIFO):
    os.mkfifo(FIFO)
while True:
    with open(FIFO) as fifo:
        for line in fifo:
            lines.append(line)
            sendMessageToBoard(hostId, ip, line)





