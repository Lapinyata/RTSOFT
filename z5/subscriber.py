import time
import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("SMART") #client creation
client.connect(mqttBroker)  #connect with broker

client.loop_start()
client.subscribe("TEST")
client.on_message = on_message
time.sleep(1000)
client.loop_end()