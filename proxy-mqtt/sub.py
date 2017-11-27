#!/bin/env python
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
import drawnow

def on_connect(client, userdata, flags, rc) :
	print("Connected with result code :" +str(rc))
	client.subscribe("sensor/temperature")
	client.subscribe("sensor/humidite")
	client.subscribe("sensor/luminosite")


def on_message(client, userdata, msg) :
	print(msg.topic+"  \t"+str(msg.payload)+"\t"+str(msg.qos)+"\n")
	if (msg.topic == 'sensor/temperature' ) :
		temp.append(int(msg.payload))
		drawnow(makeFig)
		plt.pause(0.000001)
		t_cnt+=1
		if (t_cnt < 50)
			temp.pop(0)
			t_cnt-=1

	elif (msg.topic == 'sensor/humidite' ) :
		hum.append(int(msg.payload))
		drawnow(makeFig)
		plt.pause(.000001)
	        h_cnt+=1
		if (h_cnt < 50) :
			hum.pop(0) 
			h_cnt-=1
	
	elif (msg.topic == 'sensor/luminosite') :
		light.append(int(msg.payload))
		drawnow(makeFig)
		plt.pause(.000001)
		l_cnt+=1
		if (l_cnt < 50) :
			light.pop(0)
			l_cnt-=1

def makeFig() :
	plt.ylim(0,512)
	plt.title("Captor Values")
	plt.plot(temp, 'ro-', label='Temperature')
	plt2=plot.twinx()
	plt2.plot(hum, 'bo-', label='Humidite')
	plt3=plot.twinx()
	plt3.plot(light, 'yo-', label='Luminosite')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

drawnow(makeFig)

client.connect("192.168.1.59", 1883, 60)
client.loop_forever()
