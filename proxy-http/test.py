import socket
import sys

from coapthon.client.helperclient import HelperClient

host="192.168.1.50"
port=5683
client=HelperClient(server=(host, port))


path="temperature"
response=client.get(path)
print(response.pretty_print())
client.stop()
