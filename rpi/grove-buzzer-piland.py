############################################################
# Simple Python program that repeatedly reads a data slot
# from Pi Land and turns a Grove Buzzer on port D3 either
# on or off depending on the data slot value.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-buzzer-piland.py
#
############################################################

import time
import grovepi
import requests
import sys

# Actuator settings
buzzer = 2                             # Buzzer connected to D2 port

# Pi Land settings
room = 777                             # room number to monitor
slot = 2                               # slot number to monitor

baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/read/" + str(slot)

grovepi.pinMode(buzzer, "OUTPUT")

while True:
  
  try:

    print "Getting:", baseurl

    response = requests.get(baseurl)

    if response.status_code == requests.codes.ok:
      print "Value:  ", response.text
    else:
      print "Error reading ", baseurl

    if response.text == "on":
      print ">> turning buzzer on"
      grovepi.digitalWrite(buzzer, 1)    # buzzer on
    else:
      print ">> turning buzzer off"
      grovepi.digitalWrite(buzzer, 0)    # buzzer off

    time.sleep(1)

  except KeyboardInterrupt:
    print "Control-C, turning buzzer off"
    grovepi.digitalWrite(buzzer, 0)     # buzzer off when Control-C terminate
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

