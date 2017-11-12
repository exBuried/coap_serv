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
	echo -e '\033[42m' '\033[30m' 'Updating Data' '\033[49m' '\e[39m';
	./getvalues.sh $remove_log;
	echo -e "\033[42m \033[30m Done : Repeating after $refresh_rate seconds \033[49m \e[39m";
	k=$((k+1));
	sleep $refresh_rate;

done;

