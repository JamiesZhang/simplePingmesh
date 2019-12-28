#! /bin/bash

#清除服务器端的文件夹重建
clearway(){
	{
		#echo $1,$2,$3
		echo "清除$1服务器上的残留文档" # 就不新建了，用的时候新建
		#$1，is the server ip
		#$2，is the start of the 目录
		scp everyclear.sh $USER@$1:~/pingmeshtest #需要打印一次密码
		#sleep 2
		ssh -t -t $RUSE@$1 "cd ~/pingmeshtest/; bash everyclear.sh $2 $3 " #需要打印一次密码
	} 

}

# #清除网关端的文件夹重建
# cleargate(){
# 	#echo $1
# 	#mkdir -p result;
# 	cd result;
# 	rm -rf *;
# 	t=`expr $1 \* $(($1 - 1))`
# 	#echo $t
# 	for ((i=1;i<=$t;i ++)) ;
# 	do  
#     	mkdir $i ;
# 	done  
# }

#main
ARRAY=($(awk '{print $0}' pinglist.txt))
mmm=0
for i in ${ARRAY[*]}
do
	((mmm++))
done
#mmm代表有多少个Ping
echo "共有$mmm个服务器"

count=1
for i in ${ARRAY[*]}
do
	{
		clearway $i $count $mmm
	} &
	#sleep 3 &
	#wait $!
	count=$[ $count + 1 ] # ????这里可能有点问题，不一定能把残留文件删全，看看再说吧
done

# {
# 	cleargate $mmm
# } &
# sleep 1 &
# wait $!

{
	killall -u $USER
} & 