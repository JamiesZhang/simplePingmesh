#clearforeach
hname=$(hostname)
echo "开始清除空间"
# rm -rf *
mm=$(($1-1))
tt=$(($1*$mm))
for((i=1;i<=$tt;i++)); # 这里缺了等号“=”就不能正常运行了，就进不去循环了
do  
	echo “rm directory $i”;
	rm -rf $i;
	# mkdir $i;
done  
echo "清除完成，退出 $hname."
#killall -u $USER   # 这个等之后看看有没有必要因为“port已经被使用的问题”加上这个killall，这个有点强劲
