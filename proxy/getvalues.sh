./coap-client-rasp -v 5 -m get -N coap://192.168.1.50/$1 | echo -e $(tail -n 1)  $(date "+%Y-%m-%d %H:%M:%S") >> values/$1.dat


