#!/usr/bin/env python

import paho.mqtt.client as mqtt
from subprocess import call
import subprocess
import sys
import time

if ( len(sys.argv) < 3 ) :
	print("Refresh rate and Number of values keeped needed")
	sys.exit(0);

refresh_rate=float(sys.argv[1])


def on_connect(client, userdata, flags ,rc):
	print("Connected with result code "+str(rc))
	#subprocess.Popen(["./update.sh","60"], shell=True)
	client.subscribe("sensor/temperature")
	client.subscribe("sensor/humidity")
	client.subscribe("sensor/luminosity")

def on_message(client, userdata, msg):
	
	if msg.payload == "!get temperature" :
		publish_values(client, 1)
	elif msg.payload == "!get humidity" :
		publish_values(client, 3)
	elif  msg.payload == "!get luminosity" :
		publish_values(client, 2)

def publish_values(client, id):
	print("Sending Values")
	if id == 1 or id == 0 : 
		file=open("values/temperature.dat", "r")
		data=file.readline(-1)
		file.close
		client.publish("sensor/temperature",data, 0, False)

	if id%2 == 0 :
		file=open("values/light.dat", "r")
        	data=file.readline(-1)
        	file.close 
        	client.publish("sensor/luminosity",data, 0, False)

	if id%3 == 0 :
		file=open("values/humidite.dat", "r")
        	data=file.readline(-1)
        	file.close 
        	client.publish("sensor/humidity",data, 0, False)

def actualize_data():
	print("Actualizing Values...")
	subprocess.call(["./getvalues.sh"],shell=True)
	#subprocess.call(["./getvalues.sh", "temperature"],shell=True)
	#subprocess.call(["./getvalues.sh", "humidite"],shell=True)
	print('Done')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message= on_message
client.connect("192.168.1.59", 1883,60)

client.loop_start()
while True :
	actualize_data()
	publish_values(client, 0)
	print("Sleeping for" +str(refresh_rate))
	time.sleep(refresh_rate)
