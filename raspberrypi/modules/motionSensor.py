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


