# A simple loop that reads values from the analog inputs of an Arduino port.
# No Arduino code is necessary - just upload the standard-firmata sketch from the examples.

import pyfirmata
import signal
import sys

# Definition of the analog pins you want to monitor e.g. (1,2,4)
PINS = [0,1]

# Do a graceful shutdown, otherwise the program will hang if you kill it.
def signal_handler(signal, frame):
    board.exit()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Connect to the board
print "Setting up the connection to the board ..."
board = pyfirmata.Arduino('/dev/ttyACM0')

# Iterator thread is needed for correctly reading analog input
it = pyfirmata.util.Iterator(board)
it.start()
 
# Start reporting for defined pins
for pin in PINS:
    board.analog[pin].enable_reporting()
 
# Loop that keeps printing values
while 1:
    for pin in PINS:
        print "Pin %i : %s" % (pin, board.analog[pin].read())
    board.pass_time(1)    



