############################################################
# Simple Python program that writes a message to the
# Grove LCD attached to one of the I2C ports.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-lcd.py
#
# Note: You need to have the Grove LCD Display driver
# program file 'grove_rgb_lcd.py' in the same directory
# as this program.
#
############################################################

import time
from grove_rgb_lcd import *

setRGB(255, 0, 0)
setText("Hello, World!\nRed")

time.sleep(2)

setRGB(0, 255, 0)
setText("Hello, World!\nGreen")

time.sleep(2)

setRGB(0, 0, 255)
setText("Hello, World!\nBlue")

time.sleep(2)

setRGB(255, 255, 255)
setText("Goodbye!")

