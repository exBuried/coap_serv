if [ -z "$1" ]; then 
	refresh_rate=60;
else
	refresh_rate=$1;
fi;

if [ -z "$2" ]; then
	remove_log=20;
else
	remove_log=$2;
fi;
k=0;
while true; do
	if [ "$k" -eq "$remove_log" ]; then
		k=0;
		rm values/*;
		echo "Old Values Removed";
	fi;

	echo ">> Updating Data <<";
	./getvalues.sh temperature;
	./getvalues.sh humidite;
	./getvalues.sh light;
	echo ">> Done : Repeating after $refresh_rate seconds <<";
	k=$((k+1));
	sleep $refresh_rate;
done;

