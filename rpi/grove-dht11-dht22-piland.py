############################################################
# Simple Python program that repeatedly reads the Grove
# Temperature & Humidity Sensor (DHT11) and Grove
# Temperature & Humidity Sensor Pro (DHT22) connected to
# GrovePi ports D8 & D7 and writes the current values
# to Pi Land. 
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    sudo python grove-dht11-dht22-piland.py
#
############################################################

import time
import requests
import grovepi
import sys

# Write the value to a specific data slot in a Pi Land room

# NOTE:  Change the room, dataslot, and devicename below to something
#        different for your own use so that everyone isn't using
#        the same data slot and overwriting each other's data.

# Pi Land settings
room      = 404                                # Room number to use (1 through 999)
dht22_slot_temp = 22                           # Data slot number to use (1 through 30)
dht22_name_temp = "Inside Temp DHT22"          # Descriptive name for your device, put '+' for space char
dht22_slot_humi = 23                           # Data slot number to use (1 through 30)
dht22_name_humi = "Inside Humidity DHT22"      # Descriptive name for your device, put '+' for space char
dht11_slot_temp = 24                           # Data slot number to use (1 through 30)
dht11_name_temp = "Inside Temp DHT11"          # Descriptive name for your device, put '+' for space char
dht11_slot_humi = 25                           # Data slot number to use (1 through 30)
dht11_name_humi = "Inside Humidity DHT11"      # Descriptive name for your device, put '+' for space char

# Sensor settings
dht22_port = 7                                 # DHT22 temp & humidity sensor is connected to port D7
dht11_port = 8                                 # DHT11 temp & humidity sensor is connected to port D8

# Other global variables
baseurl = "http://piland.socialdevices.io"
dht22_temp_baseurl = baseurl + "/" + str(room) + "/write/" + str(dht22_slot_temp) + "?name=" + dht22_name_temp + "&value="
dht22_humi_baseurl = baseurl + "/" + str(room) + "/write/" + str(dht22_slot_humi) + "?name=" + dht22_name_humi + "&value="
dht11_temp_baseurl = baseurl + "/" + str(room) + "/write/" + str(dht11_slot_temp) + "?name=" + dht11_name_temp + "&value="
dht11_humi_baseurl = baseurl + "/" + str(room) + "/write/" + str(dht11_slot_humi) + "?name=" + dht11_name_humi + "&value="

while True:
  
  try:

    # Read the temperature and humidity from both sensors

    [dht22_temp, dht22_humi] = grovepi.dht(dht22_port, 1)                   # second parameter:  1 = DHT22 sensor
    [dht11_temp, dht11_humi] = grovepi.dht(dht11_port, 0)                   # second parameter:  0 = DHT11 sensor

    dht22_temp_url = dht22_temp_baseurl + "%0.1f" % dht22_temp + "+C"
    dht22_humi_url = dht22_humi_baseurl + "%0.1f" % dht22_humi  + "+%25"    #  %25 will display as % sign
    dht11_temp_url = dht11_temp_baseurl + "%0.1f" % dht11_temp + "+C"
    dht11_humi_url = dht11_humi_baseurl + "%0.1f" % dht11_humi  + "+%25"    #  %25 will display as % sign

    print dht22_temp_url
    print dht22_humi_url
    print dht11_temp_url
    print dht11_humi_url

    requests.get(dht22_temp_url)    # write data
    requests.get(dht22_humi_url)    # write data
    requests.get(dht11_temp_url)    # write data
    requests.get(dht11_humi_url)    # write data

    time.sleep(2.0)           # 2 second delay

  except KeyboardInterrupt:
    print "Terminating"
    break
  except IOError:
    print "IOError, continuing"
  except:
    print "Unexpected error, continuing"
    print "sys.exc_info()[0]: ", sys.exc_info()[0]

