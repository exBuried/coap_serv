#!/usr/bin/env python
import requests as req
from collections import deque
import time
from sys import argv
from sys import exit
import matplotlib.pyplot as plt
class RealtimePlot:
	def __init__(self, axes, max_entries = 100):
		self.axis_x = deque(maxlen=max_entries)
		self.axis_y = deque(maxlen=max_entries)
		self.axes = axes
		self.max_entries = max_entries
		self.lineplot, = axes.plot([], [], "ro-")
		self.axes.set_autoscaley_on(True)

	def add(self, x, y):
		self.axis_x.append(x)
		self.axis_y.append(y)
		self.lineplot.set_data(self.axis_x, self.axis_y)
		self.axes.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
		self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis

	def animate(self, figure, callback, interval = 50):
		import matplotlib.animation as animation
		def wrapper(frame_index):
			self.add(*callback(frame_index))
			self.axes.relim(); self.axes.autoscale_view() # rescale the y-axis
			return self.lineplot
		animation.FuncAnimation(figure, wrapper, interval=interval)
def main() :

	temperature=[]
	humidite=[]


	if len(argv)==3 :
		addr=argv[1]
		refresh=argv[2]
	else :
		print("Address + Refresh Rate Needed")
		exit(0)
	light_addr=addr + "/luminosite"
	temp_addr=addr + "/temperature"
	hum_addr=addr + "/humidite"

	display = RealtimePlot(axes)

	fig,axes = plt.subplots()
	while true :
		l=req.get(light_addr)
		light=l.rsplit('\t')[0]

		t=req.get(temp_addr)
		temperature.append(t.rsplit('\t')[0])

		h=req.get(hum_addr)
		humidite.append(h.rsplit('\t')[0])

		time=l.rsplit('\t')[1]
		display.add(time, light)
		time.sleep(refresh)
if __name__ == "__main__" : main()
