
for req in light temperature humidite

do
	touch values/$req.dat
	data=$(./coap-client-rasp -v 5 -m get -N coap://192.168.1.50/$req | echo $(tail -n 1) "\t$(date "+%H:%M:%S %d-%m-%Y")")
	echo -e "$(echo $data)\n$(cat values/$req.dat)" > values/$req.dat
done

