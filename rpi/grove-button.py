############################################################
# Simple Python program that repeatedly reads a
# Grove Button attached to port D3.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-button.py
#
############################################################

import time
import grovepi
import sys

# Sensor settings
button = 3                             # button connected to D3 port

# Button debouncing
last = -1                              # last button reading
debounce = 0                           # debounce count
debounce_max = 2                       # debounce threshold
state = -1                             # stable state 

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

    last = reading

    time.sleep(0.1)

  except KeyboardInterrupt:
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

