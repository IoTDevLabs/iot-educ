############################################################
# Simple Python program that repeatedly reads a data slot
# from Pi Land and turns a Grove Relay on port D5 either
# on or off depending on the data slot value.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-led-piland.py
#
############################################################

import time
import grovepi
import requests
import sys

# Actuator settings
relay = 5                              # relay connected to D5 port

# Pi Land settings
room = 777                             # room number to monitor
slot = 3                               # slot number to monitor

baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/read/" + str(slot)

grovepi.pinMode(relay, "OUTPUT")

while True:
  
  try:

    print "Getting:", baseurl

    response = requests.get(baseurl)

    if response.status_code == requests.codes.ok:
      print "Value:  ", response.text
    else:
      print "Error reading ", baseurl

    if response.text == "on":
      print ">> turning relay on"
      grovepi.digitalWrite(relay, 1)     # relay on
    else:
      print ">> turning relay off"
      grovepi.digitalWrite(relay, 0)     # relay off

    time.sleep(1)

  except KeyboardInterrupt:
    print "Control-C, turning relay off"
    grovepi.digitalWrite(relay , 0)      # relay off when Control-C terminate
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

