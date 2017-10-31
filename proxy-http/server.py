from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if (self.path=="/") :
       		with open("values/temperature.dat", "r") as f :
       			res="Temperature\t" + f.readline()
        		self.wfile.write(res)
                with open("values/humidite.dat", "r") as f :
                	res="Humidite\t" + f.readline()
                	self.wfile.write(res)
                with open("values/light.dat", "r") as f :
                	res="Luminosite\t" + f.readline()
                	self.wfile.write(res)
                                                                        
	elif (self.path=="/temperature") :
		with open("values/temperature.dat", "r") as f :
			self.wfile.write(f.readline())
	elif (self.path=="/humidite") :               
		 with open("values/humidite.dat", "r") as f :
                        self.wfile.write(f.readline())
	elif (self.path=="/luminosite") :
                with open("values/light.dat", "r") as f :
                        self.wfile.write(f.readline())
	else :
		self.wfile.write("404 : Try [ /temperatue | /humidite | /luminosite ]")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("POST!")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=8080)


