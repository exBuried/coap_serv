#!/bin/env python
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *

global temp
temp=[]
global hum
hum=[]
global light
light=[]

t_cnt=0
h_cnt=0
l_cnt=0

plt.ion()

def makeFig() :
	global temp, hum, light
	plt.xlim(0,50)
	plt.ylim(0,100)
	plt.ylabel('Temperature & Humidity')
	plt.title("Captor Values")
	plt.plot(temp, 'ro-', label='Temperature')
	plt.plot(hum, 'bo-', label='Humidite')

	plt2=plt.twinx()
	plt2.set_ylabel('Luminosite')
	plt.xlim(0,50)
	plt.ylim(0,700)
	plt2.plot(light, 'yo-', label='Luminosite')


def on_connect(client, userdata, flags, rc) :
	print("Connected with result code :" +str(rc))
	client.subscribe("sensor/temperature")
	client.subscribe("sensor/humidite")
	client.subscribe("sensor/luminosite")


def on_message(client, userdata, msg) :
	global t_cnt, h_cnt, l_cnt
	global temp, hum, light
	print(msg.topic+"  \t"+str(msg.payload)+"\t"+str(msg.qos)+"\n")
	if (msg.topic == 'sensor/temperature' ) :
		temp.append(msg.payload)
		drawnow(makeFig)
		plt.pause(0.000001)
		t_cnt+=1
		if (t_cnt < 50) :
			temp.pop(0)
			t_cnt-=1

	elif (msg.topic == 'sensor/humidite' ) :
		hum.append(msg.payload)
		drawnow(makeFig)
		plt.pause(.000001)
		h_cnt+=1
		if (h_cnt < 50) :
			hum.pop(0)
			h_cnt-=1

	elif (msg.topic == 'sensor/luminosite') :
		light.append(msg.payload)
		drawnow(makeFig)
		plt.pause(.000001)
		l_cnt+=1
		if (l_cnt < 50) :
			light.pop(0)
			l_cnt-=1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("192.168.1.59", 1883, 60)
client.loop_forever()
