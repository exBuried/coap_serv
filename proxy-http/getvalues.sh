remove_log=20
if [ -z $1 ]
	then remove_log=19

else remove_log=$1
fi

for req in light temperature humidite

do
	touch values/$req.dat
	data=$(./coap-client-rasp -v 5 -m get -N coap://192.168.1.50/$req | echo $(tail -n 1) "\t$(date "+%H:%M:%S\t%d-%m-%Y")")
	echo -e "$(echo $data)\n$(head -$remove_log values/$req.dat)" > values/$req.dat
done


