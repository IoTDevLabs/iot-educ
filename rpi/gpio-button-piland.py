############################################################
#
# Python program that repeatedly reads a button connected to
# Raspberry Pi GPIO 17 (physical pin 11 on Pi GPIO connector)
# and writes on/off state to a Pi Land data slot. Also
# increments a counter in a second Pi Land data slot that
# counts how many times the button is pressed. The counter
# is cleared to 0 each time the program starts.
#
# The button should be normally open with one side connected
# to GPIO 17 (pin 11) and the other side connected to
# GND (pin 6 or pin 9, either pin is GND). A 10K pull-up
# resistor (brown-black-orange color bands) also needs to be
# connected between pin 11 (GPIO 17) and pin 1 (3.3V)
# otherwise the switch will generate spurious open/closed
# readings when it isn't being pressed.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python gpio-button-piland.py
#
# Press Control-C to stop the program.
#
############################################################

# Button debouncing can be adjusted by changing the value
# of debounce_max and/or the time delay in the read loop.
# Test your button to find the optimum settings for speed
# versus accurate reading of press & release.

# Python packages used in the program.
# The 'requests' package needs to be installed on your
# Pi using this command: sudo pip install requests.
import requests                # This package needs to be installed on Pi
import time                    # Built-in package; no need to install
import sys                     # Built-in package; no need to install
import RPi.GPIO as GPIO        # Should already be installed on Pi

# The Button class handles operations for one button.

class Button:

  def __init__(self, name, gpio, room, onoff_slot, counter_slot, onoff_label, counter_label):
    # Initialize the object's internal variables
    self.name = name
    self.gpio_number = gpio
    self.room = room
    self.onoff_slot = onoff_slot
    self.counter_slot = counter_slot
    self.onoff_label = onoff_label
    self.counter_label = counter_label
    self.reading = -1
    self.reading_previous = -1
    self.debounce_counter = 0
    self.debounce_max = 2
    self.stable_state = -1

  def init_gpio(self):
    # Function to initialize a button's GPIO pin
    GPIO.setmode(GPIO.BCM)                   # Set BCM pin numbering scheme
    GPIO.setwarnings(False)
    GPIO.setup(self.gpio_number, GPIO.IN)    # Set pin as input

  def init_counter(self):
    # Function to initialize button counter slot
    url = baseurl_incr_init % (self.room, self.counter_slot, self.counter_label)
    print url
    requests.get(url)                        # Call Pi Land API

  def read_button(self):
    # Function to read and debounce button, and update values in Pi Land
    self.reading = GPIO.input(self.gpio_number)      # Read current state of button GPIO pin
    if self.reading != self.reading_previous:
      self.debounce_counter = 0                      # Reset debounce counter to 0
    else:
      if self.debounce_counter < self.debounce_max:
        self.debounce_counter = self.debounce_counter + 1
      if self.debounce_counter == self.debounce_max:
        # We have stable 0->1 or 1->0 transition
        self.stable_state = self.reading
        print self.name + " = " + str(self.stable_state)
        self.debounce_counter = self.debounce_max + 1   # Set to max+1 so won't trigger again
        # Set button on/off state in Pi Land slot
        if self.stable_state == 0:       # Button is ON (0 = on)
          # Increment button counter in Pi Land slot
          sendurl = baseurl_incr % (self.room, self.counter_slot, self.counter_label)
          print sendurl                  # Print the API call URL
          requests.get(sendurl)          # Call Pi Land API to increment button counter
          sendurl = baseurl_write % (self.room, self.onoff_slot, self.onoff_label, "on")
        else:                            # Button is OFF (1 = off)
          sendurl = baseurl_write % (self.room, self.onoff_slot, self.onoff_label, "off")

        print sendurl                    # Print the API call URL
        requests.get(sendurl)            # Call Pi Land API to set button on/off state in slot

    self.reading_previous = self.reading

# Pi Land REST API endpoint URLs

baseurl = "http://piland.socialdevices.io"
baseurl_write = baseurl + "/%d/write/%d?name=%s&value=%s"
baseurl_incr  = baseurl + "/%d/incr/%d?name=%s"
baseurl_incr_init = baseurl + "/%d/write/%d?name=%s&value=0"

# Button variables

button1 = Button("button1", 17, 404, 13, 14, "Button1+Status", "Button1+Counter")

# Main program

button1.init_gpio()                       # Initialize button 1 GPIO pin

print "Button GPIO pins initialized"

button1.init_counter()                    # Initialize button 1 counter

print "Button counters cleared to 0"

# Endless loop reading button and updating Pi Land data

print "Entering endless loop"

while True:                              # Endless loop until press Control-C

  try:

    button1.read_button()                # Read and process button 1

    time.sleep(0.01)                     # Short delay until read buttons again

  except KeyboardInterrupt:              # Handle Control-C
    print ""
    print "Control-C: Terminating endless loop"
    break                                # Exit the endless loop
  except IOError:                        # Handle I/O error exception
    print "IOError, continuing"
    # Continue executing loop
  except:                                # Handle any other exception
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]
    # Continue executing loop

# Get here when exit the endless loop

GPIO.cleanup()                           # De-initialize our GPIO settings
print "GPIO pins reset"

# Program ends and will exit here

