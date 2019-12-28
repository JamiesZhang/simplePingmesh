#clearforeach

echo "开始清除空间"
# rm -rf *
for ((i=$1; i<$[$2+$1+1]; i ++))  
do  
	echo $i;
	rm -rf $i;
	# mkdir $i;
done  
echo "清除完成，退出."
killall -u $USER
