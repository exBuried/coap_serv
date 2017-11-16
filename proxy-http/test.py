import socket
import sys
import logging
from coapthon.client.helperclient import HelperClient

logging.basicConfig()
host="192.168.1.50"
port=5683
client=HelperClient(server=(host, port))


path="temperature"
response=client.get(path)
print("didiejd")
print(response.pretty_print())
client.stop()
