############################################################
# Simple Python program that repeatedly reads the Grove
# Light Sensor connected to GrovePi Analog port A1 and
# writes the current value to Pi Land.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-light-piland.py
#
############################################################

import time
import requests
import grovepi
import sys

# Write the value to a specific data slot in a Pi Land room

# NOTE:  Change the room, dataslot, and devicename below to something
#        different for your own use so that everyone isn't using
#        the same data slot and overwriting each other's data.

# Pi Land settings
room = 404                             # Room number to use (1 through 999)
slot = 8                               # Data slot number to use (1 through 30)
name = "Light Level"                   # Descriptive name for your device, put '+' for space char

# Sensor settings
light = 1                              # Light sensor is connected to Analog port A1

# Other global variables
baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="

while True:

  try:

    # Read the light level from the sensor

    light_level = grovepi.analogRead(light)

    url = baseurl + "%d" % light_level

    print url

    requests.get(url)    # write data

    time.sleep(2.0)      # 2 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]