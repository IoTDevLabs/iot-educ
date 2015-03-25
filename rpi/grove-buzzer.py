############################################################
# Simple Python program that repeatedly beeps a
# Grove Buzzer attached to port D2.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-buzzer.py
#
############################################################

import time
import grovepi

# Actuator settings
buzzer = 2                             # Buzzer connected to D2 port

grovepi.pinMode(buzzer, "OUTPUT")

while True:
  
  try:
    grovepi.digitalWrite(buzzer, 1)    # buzzer on
    print "buzzer on"
    time.sleep(0.5)

    grovepi.digitalWrite(buzzer, 0)    # buzzer off
    print "buzzer off"
    time.sleep(0.5)

  except KeyboardInterrupt:
    grovepi.digitalWrite(buzzer, 0)
    break
  except IOError:
    print "IOError"

