#process network traffic import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

MOUNT_PIN = 20
DOOR_PIN = 21

GPIO.setup(MOUNT_PIN, GPIO.OUT)
GPIO.setup(DOOR_PIN, GPIO.OUT)

MOUNT = GPIO.PWM(MOUNT_PIN,50)
DOOR = GPIO.PWM(DOOR_PIN, 50)

# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Actuator Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('motion')
    client.subscribe('dropbox')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.payload == 'Motion Detected':
        print("Motion Detected: Disbursing Drone")
        #INTERLOCK DOOR UNLOCKS
        DOOR.start(11.5)
        time.sleep(1)
        DOOR.stop()
        GPIO.cleanup()
        
        #TURN DRONE ON
        #publish.single("drone", "Start Drone", hostname="test.mosquitto.org")
        client.publish('drone', 'Start Drone');
        #WAIT 4
        time.sleep(4)
        
        #LATCH
        MOUNT.start(11.5)
        time.sleep(1)
        MOUNT.stop()
        
    elif ((msg.payload == 'Reset Mount') & (msg.topic == 'dropbox')):
        print("Message Received" + msg.topic+" "+str(msg.payload))
        MOUNT.start(7)
        time.sleep(1)
        MOUNT.stop()
  
    elif ((msg.payload == 'Reset Door') & (msg.topic == 'dropbox')):
        DOOR.start(7)
        time.sleep(1)
        DOOR.stop()

def on_subscribe(client, userdata, flags, rc):
    print("Subscribed to motion and dropbox topics.")

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
 
client.connect("test.mosquitto.org", 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
client.loop_forever()

KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
