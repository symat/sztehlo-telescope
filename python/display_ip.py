
import board
import busio
import adafruit_ssd1306
import digitalio
import time
from PIL import Image, ImageDraw, ImageFont


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




import netifaces
import ipaddress
import socket

def get_local_non_loopback_ipv4_addresses():
    for interface in netifaces.interfaces():
        # Not all interfaces have an IPv4 address:
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            # Some interfaces have multiple IPv4 addresses:
            for address_info in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address_object = ipaddress.IPv4Address(str(address_info['addr']))
                if not address_object.is_loopback:
                    yield address_info['addr']

ip_text = ','.join(list(get_local_non_loopback_ipv4_addresses()))



# Draw Text
 
(font_width, font_height) = font.getsize("H")
y = 2 * BORDER
draw.text((2 * BORDER, y), "Sztehlo Telescope", font=font, fill=255)
y += font_height
draw.text((2 * BORDER, y), "HOST: " + socket.gethostname(), font=font, fill=255)
y += font_height
draw.text((2 * BORDER, y), "IP: " + ip_text, font=font, fill=255)


# Display image
oled.image(image)
oled.show()
