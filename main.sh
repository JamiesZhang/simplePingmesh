#!/bin/bash
###测试循环读取,号前后数据
pirntpinglist(){
	for j in ${list[*]}
	{
		arr=(${j//,/ })  
		for i in ${arr[*]}
		do
			echo $i 
		done
	}
}


#ping的函数
pingagentserver(){
	{
	    echo "第 $1 对测试 "
	    echo "目标：实现server $2 启动"	
	    echo " "
		{
			echo " "
			echo "我开启了新后台,来设置$2 server" 
			echo " "
			ssh -t -t $USER@$2  "cd pingmeshtest; bash server.sh $1 $2 "
		}
		sleep 1
		#wait $!
	} &
}


pingagentclient(){
	echo " "
	echo "目标：实现client $2 启动"	
	echo " "

	sleep 5
	# {
	echo " "
	echo "我开启了新后台,来链接$3" 
	echo " "
	ssh -t -t $USER@$2 "cd pingmeshtest; bash client.sh $1 $2 $3"
	# }
	# wait $!
	echo " "
	mkdir -p result
	scp $USER@$3:~/pingmeshtest/$1/result.json result/$1	
	echo " "
	echo " "
	echo "已经成功的从$3ping$2中得到数据，并且($3 as server $2 as client)"
	echo " "
	#} &

}

#Main function 调用函数，跑测试并获得程序，主函数在这里看过来

mmm=0
ARRAY=($(awk '{print $0}' pinglist.txt))
{
	for i in ${ARRAY[*]}
	do
		echo ${i}
		scp server.sh $USER@$i:~/pingmeshtest
		scp client.sh $USER@$i:~/pingmeshtest
		scp s.cpp $USER@$i:~/pingmeshtest
		scp c.cpp $USER@$i:~/pingmeshtest
		((mmm=mmm+1))
	done
}
# wait $!
echo "";
echo "一共" $mmm "台服务器";
echo "";


#创建ping的数组队列，,号隔开，前面server，后面client :并创建对应文档用于记录ping数据。
idd=1
for m in ${ARRAY[*]}
{
	for n in ${ARRAY[*]}
	do
		if [ $m != $n ];then
			list[idd]="$m,$n"
			((idd++))
		fi
	done
}

pingthesame(){
	j=${list[$1]}
	arr=(${j//,/ }) # arr = 分隔开
	s=${arr[0]}; 	# s = server部分 
	c=${arr[1]};  	# c= client部分
	pingagentserver $1 $s
	sleep 2
	{
		pingagentclient $1 $c $s; 
	}
}

tt=$(($mmm*$(($mmm-1))))
ddd=1;
# ddd记录一共有几对互ping
while(($ddd<=$tt))
do 
	pingthesame $ddd
	$ddd=$ddd+1
	echo $ddd
done
