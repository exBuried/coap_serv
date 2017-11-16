#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import socket
import sys
import logging
from coapthon.client.helperclient import HelperClient

logging.basicConfig()

coap_host="192.168.1.50"
coap_port=5683
client=HelperClient(server=(host, port))

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		light_val=
		temp_val=
		hum_val=
		self._set_headers()

		path=self.path.split("/")
		if (path[0]=="/") :
			res="Temperature\t" + temp_val
			self.wfile.write(res)
			res="Humidite\t" + hum_val
			self.wfile.write(res)
			res="Luminosite\t" + light_val
			self.wfile.write(res)

		elif (path[0]="/update")

		elif (path[0]=="/temperature") :
			if (len(path)==1):
				self.wfile.write(temp_val)

			else if 


		elif (path[0]=="/humidite") :
			if (len(path)==1):
				self.wfile.write(hum_val)
			else :


		elif (path[0]=="luminosite") :
			if (len(path)==1):
				self.wfile.write(light_val)
			else :

		else :
			self.wfile.write("404 : Try [ /temperatue | /humidite | /luminosite ]")

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		self._set_headers()
		self.wfile.write("POST!")


def run(server_class=HTTPServer, handler_class=S, port=80):

	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('Starting httpd...')
	httpd.serve_forever()

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run(port=8080)
