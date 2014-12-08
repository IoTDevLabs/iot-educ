############################################################
# Simple Python program that reads the Raspberry Pi's
# internal CPU temperature sensor and prints the value
# in degrees Celsius and degrees Fahrenheit.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    python read-cpu-temp.py 
#
############################################################

# Read the temperature value

rawtemp = open("/sys/class/thermal/thermal_zone0/temp").read()

# Convert to the units we want

tempC = float(rawtemp) / 1000.0
tempF = (tempC * 1.8) + 32

# Print values to the terminal

print "temp = %7.3f degrees C" % tempC
print "temp = %7.3f degrees F" % tempF

