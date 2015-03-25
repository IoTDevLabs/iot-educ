############################################################
# Simple Python program that repeatedly reads a
# Grove Button attached to port D3 and writes the
# on/off state to Pi Land.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-button-piland.py
#
############################################################

import time
import requests
import grovepi
import sys

# Sensor settings
button = 3                             # button connected to D3 port

# Button debouncing
last = -1                              # last button reading
debounce = 0                           # debounce count
debounce_max = 2                       # debounce threshold
state = -1                             # stable state 

# Pi Land settings
room = 404                             # Room number to use (1 through 999)
slot = 11                              # Data slot number to use (1 through 30)
name = "Button"                        # Descriptive name for your device, put '+' for space char

baseurl = "http://piland.socialdevices.io"
baseurl = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="

grovepi.pinMode(button, "INPUT")

while True:
  
  try:

    reading = grovepi.digitalRead(button)

    # debouncing logic

    if reading != last:
      debounce = 0
    else:
      if debounce < debounce_max:
        debounce += 1
      elif debounce == debounce_max:
        # have a state transition
        state = reading
        print "button =", state
        debounce = debounce_max + 1 
        if state == 0:
          # switch is off
          sendurl = baseurl + "off"
        else:
          # switch is on
          sendurl = baseurl + "on"

        print sendurl

        requests.get(sendurl)

    last = reading

    time.sleep(0.1)

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

