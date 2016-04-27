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
# connected between pin 11 (GPIO 17) and pin 6 or pin 9
# (GND) otherwise the switch will generate spurious
# open/closed readings when it isn't being pressed.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python gpio-button-piland.py
#
# Press Control-C to stop the program.
#
############################################################

# Button debouncing can be adjusted by changing the values
# of button1_debounce_max and/or button1_debounce_delay.
# Test your button to find the optimum settings for speed
# versus accurate reading of press & release.

# Python packages used in the program.
# The 'requests' package needs to be installed on your
# Pi using this command: sudo pip install requests.
import requests                # This package needs to be installed on Pi
import time                    # Built-in package; no need to install
import sys                     # Built-in package; no need to install
import RPi.GPIO as GPIO        # Should already be installed on Pi

# Sensor settings
button1_gpio_number = 17       # Button 1 connected to GPIO 17 (pin 11) 

# Button debouncing
button1_reading = -1           # Current reading from hardware pin
button1_reading_previous = -1  # Previous reading from hardware pin
button1_debounce_counter = 0   # Debounce counter
button1_debounce_max = 2       # How many consecutive readings of same 0 or 1 state are needed
button1_debounce_delay = 0.01  # Time (in seconds) to wait between button readings
button1_stable_state = -1      # Debouced (stable) reading of the button

# Pi Land room
piland_room = 404              # Room number to use (1 through 999)

# Pi Land slots for each button 
button1_onoff_slot = 13                   # Slot to put button1 on/off state
button1_counter_slot = 14                 # Slot number to put button1 press counter
button1_onoff_label = "Button1+Status"    # Label for button on/off slot; '+' will be space
button1_counter_label = "Button1+Counter" # Label for button on/off slot; '+' will be space

# Pi Land REST API endpoint URLs
baseurl = "http://piland.socialdevices.io"
baseurl_write = baseurl + "/" + str(piland_room) + "/write/%d?name=%s&value=%s"
baseurl_incr  = baseurl + "/" + str(piland_room) + "/incr/%d?name=%s"
baseurl_incr_init = baseurl + "/" + str(piland_room) + "/write/%d?name=%s&value=0"

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)                    # Set BCM pin numbering scheme
GPIO.setwarnings(False)
GPIO.setup(button1_gpio_number, GPIO.IN)  # Set Button1 pin as input
print "GPIO pins initialized"

# Initialize button counter to 0

# Button 1
resturl = baseurl_incr_init % (button1_counter_slot, button1_counter_label)
print resturl                             # Print the API call URL
requests.get(resturl)                     # Call Pi Land API
print "Button1 counter cleared to 0"

# Endless loop reading button and updating Pi Land data

do_incr = False

print "Entering endless loop"

while True:                               # Endless loop until press Control-C
  
  try:

    # Read and debounce button 1

    button1_reading = GPIO.input(button1_gpio_number)     # Read current state of button GPIO pin

    # Debouncing logic

    if button1_reading != button1_reading_previous:
      button1_debounce_counter = 0                        # Reset debounce counter to 0
    else:
      if button1_debounce_counter < button1_debounce_max:
        button1_debounce_counter = button1_debounce_counter + 1
      if button1_debounce_counter == button1_debounce_max:
        # We have stable 0->1 or 1->0 transition
        button1_stable_state = button1_reading
        print "button1 =", button1_stable_state
        button1_debounce_counter = button1_debounce_max + 1   # Set to max+1 so won't trigger again
        # Set button on/off state in Pi Land slot
        if button1_stable_state == 0:    # Button is ON (0 = on) 
          sendurl = baseurl_write % (button1_onoff_slot, button1_onoff_label, "on")
          do_incr = True                 # When button off -> on we should increment the counter
        else:                            # Button is OFF (1 = off) 
          sendurl = baseurl_write % (button1_onoff_slot, button1_onoff_label, "off")

        print sendurl                    # Print the API call URL
        requests.get(sendurl)            # Call Pi Land API to set button on/off state in slot

        if do_incr == True:
          do_incr = False
          # Increment button counter in Pi Land slot
          sendurl = baseurl_incr % (button1_counter_slot, button1_counter_label)
          print sendurl                  # Print the API call URL
          requests.get(sendurl)          # Call Pi Land API to increment button counter

    button1_reading_previous = button1_reading

    time.sleep(button1_debounce_delay)   # Short delay until read button again

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

