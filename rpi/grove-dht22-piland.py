############################################################
# Simple Python program that repeatedly reads the Grove
# Temperature & Humidity Sensor Pro (DHT22) connected to
# GrovePi port D7 and writes the current value to Pi Land. 
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    python grove-dht22-piland.py
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
room      = 404                          # Room number to use (1 through 999)
slot_temp = 22                           # Data slot number to use (1 through 30)
name_temp = "Inside Temp DHT22"          # Descriptive name for your device, put '+' for space char
slot_humi = 23                           # Data slot number to use (1 through 30)
name_humi = "Inside Humidity DHT22"      # Descriptive name for your device, put '+' for space char

# Sensor settings
dht22_port = 7                           # DHT22 temp & humidity sensor is connected to port D7

# Other global variables
baseurl = "http://piland.socialdevices.io"
temp_baseurl = baseurl + "/" + str(room) + "/write/" + str(slot_temp) + "?name=" + name_temp + "&value="
humi_baseurl = baseurl + "/" + str(room) + "/write/" + str(slot_humi) + "?name=" + name_humi + "&value="

while True:
  
  try:

    # Read the temperature and humidity

    [temp, humi] = grovepi.dht(dht22_port, 1)               # second parameter:  1 = DHT22 sensor

    temp_url = temp_baseurl + "%0.1f" % temp + "+C"
    humi_url = humi_baseurl + "%0.1f" % humi  + "+%25"      #  %25 will display as % sign

    print temp_url
    print humi_url

    requests.get(temp_url)    # write data
    requests.get(humi_url)    # write data

    time.sleep(2.0)           # 2 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"

