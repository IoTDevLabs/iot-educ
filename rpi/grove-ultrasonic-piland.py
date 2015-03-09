############################################################
# Simple Python program that repeatedly reads the Grove
# Ultrasonic Ranger connected to GrovePi port D4 and
# writes the current value to Pi Land. 
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    python grove-ultrasonic-piland.py
#
############################################################

import time
import requests
import grovepi

# Write the value to a specific data slot in a Pi Land room

# NOTE:  Change the room, dataslot, and devicename below to something
#        different for your own use so that everyone isn't using
#        the same data slot and overwriting each other's data.

# Pi Land settings
room = 404                             # Room number to use (1 through 999)
slot = 21                              # Data slot number to use (1 through 30)
name = "Distance"                      # Descriptive name for your device, put '+' for space char

# Sensor settings
ranger = 4                             # Ultrasonic Ranger is connected to port D4

# Other global variables
baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="

while True:
  
  try:

    # Read the ultrasonic ranger distance

    distance_cm = grovepi.ultrasonicRead(ranger)

    url = baseurl + "%d" % distance_cm + "+cm"

    print url

    requests.get(url)    # write data

    time.sleep(2.0)      # 2 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError"

