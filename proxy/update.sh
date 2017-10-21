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
	if [ $k = remove_log ]; then
		k=0;
		rm values/*;
	fi;

	echo -e "\e[32mUpdating Data\e[39m";
	./getvalues.sh temperature;
	./getvalues.sh humidite;
	./getvalues.sh light;
	echo -e "\e[32mDone : Repeating after $1 seconds\e[39m";
	k=$((k+1));
	sleep $refresh_rate;
done;

