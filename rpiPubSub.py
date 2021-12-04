"""EE 250L Lab 04 Starter Code
Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *

USERNAME = "kaley-zuoning"
led_light = 3 # LED light at D3
ultrasonic_ranger = 4 # Ultrasonic Ranger at port D4
button = 7 # button at D7
threshold = 20

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    
    #subscribe to topics of interest here
    # client.subscribe(USERNAME + "/ultrasonicRanger")
    client.subscribe(USERNAME + "/lcd")
    client.message_callback_add(USERNAME+"/lcd", lcd_callback)
    #client.subscribe(USERNAME + "/led")
    #client.message_callback_add(USERNAME+"/led", led_callback)


def lcd_callback(client, userdata, message):
    msg = str(message.payload.decode())
    print(msg)
    
    setRGB(0,0,255)
    #setCursor(0,0)
    
    if msg == "":
        setText("ERROR")
    else:
        txts = msg.split('$', 1)
        setText(txts[0][:15] + "\n" + txts[1][0:5] + "% RAM usage")
      #  setText('\n' + txts[1])
    
    print(txts[1])
    
    print(type(txts[1]))
    
    #percent = int(txts[1])
    
    if parseInt(txts[1]) > threshold:
        print("above threshold")
        setRGB(255,0,0)
    else:
        print("below threshold")
        setRGB(0,255,0)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#def led_callback(client, userdata, message):
#     print(str(message.payload))
#    if str((message.payload).decode()) == "LED_ON":
#        digitalWrite(led_light, 1)
#    elif str((message.payload).decode()) == "LED_OFF":
#        digitalWrite(led_light, 0)
#    else:
#        print("Invalid format")
    # topic = message.topic
    # command = ""
    # if topic == "led":
    #     command = topic.payload
    #     if command == "LED_ON":



if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()


    pinMode(led_light, "OUTPUT")
    pinMode(button, "INPUT")

    while True:
#         print("delete this line")
        time.sleep(1)

        distance = ultrasonicRead(ultrasonic_ranger)
        client.publish(USERNAME+"/ultrasonicRanger", str(distance))
        button_status = digitalRead(button)
        if button_status: # button ON
            client.publish(USERNAME+"/button", "Button pressed!")
