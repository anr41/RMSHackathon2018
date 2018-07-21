import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

INTERLOCK_PIN = 20
LATCH_PIN = 21

GPIO.setup(INTERLOCK_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)

# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Actuator Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ASSDRONE/Sensor/Alarm")
 

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.payload == "Motion Detected":
        print("Motion Detected: Disbursing Drone")
        #INTERLOCK
        #TURN DRONE ON
        #WAIT 10
        #LATCH
    else 
        print("Message Received" + msg.topic+" "+str(msg.payload))

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
 
client.connect("test.mosquitto.org", 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()


