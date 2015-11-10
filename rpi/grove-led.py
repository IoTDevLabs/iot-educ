############################################################
# Simple Python program that repeatedly blinks a
# Grove LED attached to port D6.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-led.py
#
############################################################

import time
import grovepi
import sys

# Actuator settings
led = 6                                # LED connected to D6 port

grovepi.pinMode(led, "OUTPUT")

while True:
  
  try:
    print "led on"
    grovepi.digitalWrite(led, 1)       # led on
    time.sleep(0.5)

    print "led off"
    grovepi.digitalWrite(led, 0)       # led off
    time.sleep(0.5)

  except KeyboardInterrupt:
    grovepi.digitalWrite(led, 0)       # turn led off Control-C terminates the program
    break
  except IOError:
    print "IOError"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

