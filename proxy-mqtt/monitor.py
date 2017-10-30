#!/usr/bin/env python

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from plot_data import DataPlot, RealtimePlot

fig, axes = plt.subplots()
plt.title("Monitor")

data=DataPlot()

dataPlotting = RealtimePlot(axes)

count=0

def on_connect(client,userdata, flags, rc):
	client.subscribe("sensor/temperature")
	client.subscribe("sensor/luminosity")
	client.subscribe("sensor/humidity")
	

def on_message(client, userdata, msg):
	if msg.
