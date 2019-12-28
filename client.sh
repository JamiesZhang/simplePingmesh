#client
echo $1,$2,$3;
echo " "

echo "现在的文件夹是" $1
echo " "
echo "现在的客户端是" $2
echo " "
echo "现在的服务器是" $3
echo " "

mkdir -p $1;

echo "当前客户端是"$2
echo "有以下文件"
ls;
cp ~/pingmeshtest/c.cpp $1/;

cd $1 ;
g++ c.cpp -o c -std=c++11;
./c $3 $2;
echo " "
echo "client $2 发送完成"
echo " "