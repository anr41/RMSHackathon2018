#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

PIR_PIN = 21
LED_PIN = 20
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

motionCount = 0
ready = 0

def on_connect(client, userdata, flags, rc):
    print('Connected to drone topic')
    client.subscribe('drone')
    client.subscribe('motion')


def on_message(client, userdata, msg):
    global ready
    print(msg.payload)
    if msg.payload == 'Drone Ready':
        ready = 1
        print('Ready' + str(ready))
        time.sleep(1)
    elif msg.payload == "Reset":
        ready = 0


try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('test.mosquitto.org',1883, 60)
    client.loop_start() 
    print ("PIR Module Test (CTRL_C to exit)")
    time.sleep(2)
    print ("ready")
    #publish.single("assdrone/sensor", "Motion Sensor Detected", hostname = "test.mosquitto.org")
    while True:
        print(str(ready) + "variable")
        if ready == 1:
            print(motionCount)        
            if GPIO.input(PIR_PIN):
               if (motionCount >= 3):
                  GPIO.output(LED_PIN,GPIO.HIGH)
                  print('Motion Detected.') 
                  client.publish('motion', 'Motion Detected') 
                  #We can expand ths to multiple drones, just have to ensure only one drone is chasing each sensor target
                  #publish.single("assdrone/sensor", "Motion Detected", hostname="test.mosquitto.org")
                  #time.sleep(1)
               motionCount = motionCount+1
            else:
                GPIO.output(LED_PIN,GPIO.LOW)
                if (motionCount > 0):            
                   motionCount = motionCount-1
            time.sleep(.25)
        else:
            motionCount = 0
            time.sleep(.25)
            
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
    
client.loop_forever()

#########################################################################
#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

PIR_PIN = 21
LED_PIN = 20
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

ready = 0
motionCount = 0

def on_connect(client, userdata, flags, rc):
    print('Connected.')
    client.subscribe('drone')

def on_message(client, userdata, msg):
    if msg.payload == "Drone Ready":
        ready = 1
    elif msg.payload == "Reset":
        ready = 0


try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect('test.mosquitto.org')
    client.loop_start() 
    print ("PIR Module Test (CTRL_C to exit)")
    time.sleep(2)
    print ("ready")
    #publish.single("assdrone/sensor", "Motion Sensor Detected", hostname = "test.mosquitto.org")
    while True:
        if ready == 1:
            print(motionCount)        
            if GPIO.input(PIR_PIN):
               if (motionCount >= 3):
                  GPIO.output(LED_PIN,GPIO.HIGH)
                  print('Motion Detected.') 
                  client.publish('motion', 'Motion Detected') 
                  #We can expand ths to multiple drones, just have to ensure only one drone is chasing each sensor target
                  #publish.single("assdrone/sensor", "Motion Detected", hostname="test.mosquitto.org")
                  #time.sleep(1)
               motionCount = motionCount+1
            else:
                GPIO.output(LED_PIN,GPIO.LOW)
                if (motionCount > 0):            
                   motionCount = motionCount-1
            time.sleep(.25)
        else:
            motionCount = 0
            time.sleep(.25)
            
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
    
client.loop_forever()

/#

import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIR_PIN = 20 
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    print "PIR Module Test (CTRL_C to exit)"
    time.sleep(2)
    print "ready"
    publish.single("assdrone/sensor", "Motion Sensor Detected", hostname = "test.mosquitto.org")
    while True:
        if GPIO.input(PIR_PIN):
            print "Motion Detected"
            #We can expand ths to multiple drones, jst have to ensure only one drone is chasing each sensor target
            publish.single("assdrone/sensor", "Motion Detected", hostname="test.mosquitto.org")
        time.sleep(1)
        
except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()


#/
