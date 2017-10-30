./coap-client-rasp -v 5 -m get -N coap://192.168.1.50/light | echo $(tail -n 1)  "[$(date "+%Y-%m-%d %H:%M:%S")]" >> values/light.dat
./coap-client-rasp -v 5 -m get -N coap://192.168.1.50/temperature | echo $(tail -n 1)  "[$(date "+%Y-%m-%d %H:%M:%S")]" >> values/temperature.dat
./coap-client-rasp -v 5 -m get -N coap://192.168.1.50/humidite | echo $(tail -n 1)  "[$(date "+%Y-%m-%d %H:%M:%S")]" >> values/humidite.dat



