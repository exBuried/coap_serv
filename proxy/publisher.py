#!/usr/bin/env python

import paho.mqtt.client as mqtt
from subprocess import call
import subprocess

def on_connect(client, userdata, flags ,rc):
	print("Connected with result code "+str(rc))
	subprocess.Popen(["./update.sh","60","60"], shell=True)
	client.subscribe("sensor/temperature")
	client.subscribe("sensor/humidity")
	client.subscribe("sensor/luminosity")

def on_message(client, userdata, msg):
	
	if msg.payload == "!get temperature" :
		publish_log(client, 1)
	elif msg.payload == "!get humidity" :
		print("coucou")
		publish_log(client, 3)
	elif  msg.payload == "!get luminosity" :
		publish_data(client, 2)
	

def publish_log(client, id):
	print("merde")
	print("Sending Values")
	if id == 1 or id == 0 : 
		file=open("values/temperature.dat", "r")
		data=file.read()
		file.close
		client.publish("sensor/temperature",data, 0, False)

	if id%2 == 0 :
		file=open("values/light.dat", "r")
        	data=file.read()
        	file.close 
        	client.publish("sensor/luminosity",data, 0, False)

	if id%3 == 0 :
		file=open("values/humidite.dat", "r")
        	data=file.read()
		print("13456")
        	file.close 
        	client.publish("sensor/humidity",data, 0, False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message= on_message
client.connect("192.168.1.59", 1883,60)
client.loop_forever()
