while true; do 
	echo  "Humidity :"
	./coap-client -B 2 -m get coap://192.168.1.50/humitie 
	echo "Temperature : "
	./coap-client -B 2 -m get coap://192.168.1.50/temperature 
	echo "Luminosity : "
	./coap-client -B 2 -m get coap://192.168.1.50/light 
	sleep 5
done
