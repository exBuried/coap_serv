#!/bin/env python
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *


plt.ion()


class MQTTCustomClass() :
	temp=[0]
	hum=[0]
	light=[0]

	def makeFig() :
		plt.xlim(0,50)
		plt.ylim(0,100)
		plt.ylabel('Temperature & Humidity')
		plt.title("Captor Values")
		plt.plot(MQTTCustomClass.temp, 'ro-', label='Temperature')


	def on_connect(client, userdata, flags, rc) :
		print("Connected with result code :" +str(rc))
		client.subscribe("sensor/temperature")
		client.subscribe("sensor/humidite")
		client.subscribe("sensor/luminosite")


	def on_message(client, userdata, msg) :

		if (msg.topic == 'sensor/temperature' ) :
			MQTTCustomClass.temp.append(msg.payload)
			print(MQTTCustomClass.temp)
			drawnow(MQTTCustomClass.makeFig)
			plt.pause(0.000001)
			if (len(MQTTCustomClass.temp) < 50) :
				MQTTCustomClass.temp.pop(0)


		elif (msg.topic == 'sensor/humidite' ) :
			MQTTCustomClass.hum.append(msg.payload)
			drawnow(MQTTCustomClass.makeFig)
			plt.pause(.000001)
			if (len(MQTTCustomClass.hum) < 50) :
				MQTTCustomClass.hum.pop(0)


		elif (msg.topic == 'sensor/luminosite') :
			MQTTCustomClass.light.append(msg.payload)
			drawnow(MQTTCustomClass.makeFig)
			plt.pause(.000001)
			if (len(MQTTCustomClass.temp) < 50) :
				MQTTCustomClass.light.pop(0)


client = mqtt.Client()
client.on_connect = MQTTCustomClass.on_connect
client.on_message = MQTTCustomClass.on_message


client.connect("192.168.1.59", 1883, 60)
client.loop_forever()
