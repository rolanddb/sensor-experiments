# A simple loop that reads values from the analog inputs of an Arduino port.
# No Arduino code is necessary - just upload the standard-firmata sketch from the examples.
#
# Mosquitto needs to run - you can test by running 'mosquitto_sub -t sensor/analog/in/+'


import pyfirmata
import mosquitto
import os
import signal
import sys

# Sensor config
PINS = [0,1] # analog pins you want to monitor e.g. (1,2,4)
frequency = 1 # how often to read

# MQTT config
broker = "127.0.0.1"
port = 1883
topic = "sensor/analog/in"

    
# Do a graceful shutdown, otherwise the program will hang if you kill it.
def signal_handler(signal, frame):
    arduino.exit()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def init_arduino():
    # Connect to the board
    board = pyfirmata.Arduino('/dev/ttyACM0')

    # Iterator thread is needed for correctly reading analog input
    it = pyfirmata.util.Iterator(board)
    it.start()

    # Start reporting for defined pins
    for pin in PINS:
        board.analog[pin].enable_reporting()

    return board


# Main program

print "Setting up the connection to the board ..."
arduino = init_arduino()

print "Connecting to Mosquitto ..."
# Connect to the MQTT broker (mosquitto)
mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)
mqttc.connect(broker, port, 60)
print "Ready ... "
 
# Loop that keeps printing values
while mqttc.loop() == 0:
    for pin in PINS:
        value = arduino.analog[pin].read()
        if value is not None: # First read after startup is typically None
            pintopic = topic + "/" + str(pin)
            print "Sensor: {0} value: {1}".format(pin, value)
            mqttc.publish(pintopic, str(value))
    arduino.pass_time(frequency) # sleep for a while   



