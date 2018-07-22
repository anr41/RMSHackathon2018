#process network traffic import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

MOUNT_PIN = 8
DOOR_PIN = 7

GPIO.setup(MOUNT_PIN, GPIO.OUT)
GPIO.setup(DOOR_PIN, GPIO.OUT)

MOUNT = GPIO.PWM(MOUNT_PIN, 50)
DOOR = GPIO.PWM(DOOR_PIN, 50)

#ready = 0
drop = 0
resetMount = 0
resetDoor = 0

# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Actuator Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('drone')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global drop
    global reset
    global resetMount
    global resetDoor
    print(msg.payload)
   # if msg.payload == 'Ready Actuator':
   #     print('Actuator Ready' + msg.payload)
   #     time.sleep(0.1)
    if msg.payload == "Reset Mount":
        print('Actuator Ready' + msg.payload)
        resetMount = 1
        resetDoor = 0
        drop = 0
    elif msg.payload == "Reset Door":
        print('Actuator Ready' + msg.payload)
        resetDoor = 1
        drop = 0
        resetMount = 0
    elif msg.payload == 'Motion Detected':
        print("Motion Detected: Disbursing Drone")
        drop = 1
        resetMount = 0
        resetDoor = 0

def on_subscribe(client, userdata, flags, rc):
    print("Subscribed to motion and dropbox topics.")

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('test.mosquitto.org',1883, 60)
    client.loop_start() 
    print ("Actuator Module Test (CTRL_C to exit)")
    time.sleep(2)
    print ("ready")
    #publish.single("assdrone/sensor", "Motion Sensor Detected", hostname = "test.mosquitto.org")
    while True:
      #  print(str(ready) + "variable")
     #   if ready == 1:
        if resetDoor == 1:
            print("Message Received " + msg.topic+" "+str(msg.payload))
            #DOOR.start(6)
            time.sleep(1)
            DOOR.start(12.5)
            time.sleep(1)
            DOOR.stop()
            time.sleep(1)
            client.publish('actuator', "door reset")
            resetDoor = 0
            resetMount = 0
            drop = 0
        elif resetMount == 1:
            print("Message Received " + msg.topic+" "+str(msg.payload))
            #MOUNT.start(7)
            time.sleep(1)
            MOUNT.start(11.2)
            time.sleep(1)
            MOUNT.stop()
            time.sleep(1)
            client.publish('actuator', "mount reset")
            resetMount = 0
            resetDoor = 0
            drop = 0
        elif drop == 1:
            #INTERLOCK DOOR UNLOCKS
            #DOOR.start(12.5)
            time.sleep(1)
            DOOR.start(6)
            time.sleep(1)
            DOOR.stop()
            #TURN DRONE ON
            #publish.single("drone", "Start Drone", hostname="test.mosquitto.org")
            client.publish('drone', 'Start Drone')
            #WAIT 4
            time.sleep(3.5)
            #LATCH
            #MOUNT.start(11.2) #2.5
            time.sleep(1)
            MOUNT.start(7)   #8
            time.sleep(1)
            MOUNT.stop()
            time.sleep(1)
            client.publish('actuator', 'dropped')
            drop = 0
            resetMount = 0
            resetDoor = 0

                
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
    
client.loop_forever()


