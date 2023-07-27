
import board
import busio
import adafruit_ssd1306
import digitalio
import time
import netifaces
import ipaddress
import socket
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import threading
import subprocess



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



BORDER = 2

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = digitalio.DigitalInOut(board.D4)
reset_pin.switch_to_output()
reset_pin.value = False
time.sleep(0.1)
reset_pin.value = True
time.sleep(0.1)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.load_default()
(font_width, font_height) = font.getsize("H")

number_of_rows = (64 - 4 * BORDER) / font_height
start_x = 2 * BORDER
start_y = 2 * BORDER


header = [
    "HOST: " + socket.gethostname(),
    "IP: " + get_ip_text()
]
lines = deque(["", "Hello!"])

def redraw(lines):
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,
        fill=0,)
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, start_y + len(header) * font_height),
        outline=255,
        fill=255,)
    y = start_y
    for line in header:
        draw.text((start_x, y), line, font=font, fill=0)
        y += font_height
    for line in lines:
        draw.text((start_x, y), line, font=font, fill=255)
        y += font_height

    # Display image
    oled.image(image)
    oled.show()



redraw(lines)

def check_oled():
    while True:
        time.sleep(1)
        completedProc = subprocess.run(['i2cget', '-y', '1', '0x3c'],
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.STDOUT)
        if completedProc.returncode != 0:
            print("unable to communicate on I2C, will return")
            os._exit(1)

checking_thread = threading.Thread(target=check_oled)
checking_thread.daemon = True

print("Starting oled checking thread")
checking_thread.start()



FIFO = '/home/pi/oled'
if not os.path.exists(FIFO):
    os.mkfifo(FIFO)
while True:
    with open(FIFO) as fifo:
        for line in fifo:
            lines.append(line)
            while len(lines) > number_of_rows - len(header):
                lines.popleft()
            redraw(lines)

