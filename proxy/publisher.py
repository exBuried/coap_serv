#!/usr/bin/env python

import paho.mqtt.client as mqtt
from subprocess import call

def on_connect(client, userdata, flags ,rc):
	print("Connected with result code "+str(rc))
	client.subscribe("sensor/temperature")
	client.subscribe("sensor/humidity")
	client.subscribe("sensor/luminosity")
def on_message(client, userdata, msg):
	if msg.payload == "!get temperature" :
		publish_data(client, 1)
	elif msg.payload == "!get humidity" :
		publish_data(client, 3)
	elif  msg.payload == "!get luminosity" :
		publish_data(client, 2)
	print(msg.topic +" " +str(msg.payload))
	
def publish_data(client, id):

	print("Sending Values")
	if id == 1 or id == 0 : 
		file=open("values/temperature.dat", "r")
		data=file.readline(-1)
		file.close
		client.publish("sensor/temperature",data, 0, True)

	if id%2 == 0 :
		file=open("values/light.dat", "r")
        	data=file.readline(-1)
        	file.close 
        	client.publish("sensor/luminosity",data, 0, True)

	if id%3 == 0 :
		file=open("values/humidite.dat", "r")
        	data=file.readline(-1)
        	file.close 
        	client.publish("sensor/humidity",data, 0, True)

def actualize_values(mosq, obj, msg):
	print("Updating Values")
	call(["./getvalues.sh","temperature"])
	call(["./getvalues.sh","humidite"])
	call(["./getvalues.sh","light"])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message= on_message
client.connect("192.168.1.59", 1883,60)
client.loop_forever()
