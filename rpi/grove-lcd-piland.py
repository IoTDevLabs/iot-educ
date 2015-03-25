############################################################
# Simple Python program that repeatedly reads a data slot
# from Pi Land and writes the name and value fields
# to a Grove LCD Display connected to one of the I2C ports.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-lcd-piland.py
#
# Note: You need to have the Grove LCD Display driver
# program file 'grove_rgb_lcd.py' in the same directory
# as this program.
#
############################################################

import time
import grovepi
from grove_rgb_lcd import *
import requests
import sys

# Pi Land settings
room = 500                             # room number to monitor
slot = 2                               # slot number to monitor

baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/read/" + str(slot)

setRGB(255, 255, 255)                  # set LCD color to white

last = ""                              # last value read from Pi Land

while True:
  
  try:

    print "Getting:", baseurl

    response = requests.get(baseurl)

    if response.status_code == requests.codes.ok:
      print "Value:  ", response.text
      if response.text != last:
        # only write to display when the value changes
        setText("On/Off Toggle:\n" + response.text)
        last = response.text
    else:
      print "Error reading ", baseurl

    time.sleep(1)

  except KeyboardInterrupt:
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

