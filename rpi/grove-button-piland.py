############################################################
# Simple Python program that repeatedly reads a
# Grove Button attached to port D3 and writes the
# on/off state to Pi Land. Also increments a counter
# of how many times the button was pressed.
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
name = "Button+Status"                 # Descriptive name for your device, put '+' for space char
slot_incr = 12                         # Data slot for incrementing counter
name_incr = "Button+Counter"           # Descriptive name for incrementing counter

baseurl = "http://piland.socialdevices.io"
baseurl_write = baseurl + "/" + str(room) + "/write/" + str(slot) + "?name=" + name + "&value="
baseurl_incr = baseurl + "/" + str(room) + "/incr/" + str(slot_incr) + "?name=" + name_incr
baseurl_incr_init = baseurl + "/" + str(room) + "/write/" + str(slot_incr) + "?name=" + name_incr + "&value=0"

grovepi.pinMode(button, "INPUT")

# Initialize the incrementing counter to 0

print baseurl_incr_init
requests.get(baseurl_incr_init)

# Endless loop reading button and updating Pi Land data

do_incr = False

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
          sendurl = baseurl_write + "off"
        else:
          # switch is on
          sendurl = baseurl_write + "on"
          do_incr = True

        print sendurl

        requests.get(sendurl)

        if do_incr == True:
          do_incr = False
          requests.get(baseurl_incr)

    last = reading

    time.sleep(0.05)

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

