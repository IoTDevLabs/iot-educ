############################################################
# Simple Python program that reads the Raspberry Pi's
# network MAC address and prints the value.
#
# To run this program from the bash command prompt,
# type this and hit Enter:
#
#    python read-mac-addr.py 
#
############################################################

# Read the MAC address

mac = open("/sys/class/net/eth0/address").read().rstrip()

# Print value to the terminal

print "mac addr = " + mac

