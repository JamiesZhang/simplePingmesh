#include <sys/types.h>  
#include <sys/socket.h>  
#include <stdio.h>  
#include <netinet/in.h>  
#include <arpa/inet.h>  
#include <unistd.h>  
#include <string.h>  
#include <stdlib.h>  
#include <fcntl.h>  
#include <sys/shm.h>  
#include <chrono>
#include <iostream>  
#include <sstream>
#include <netdb.h>
#include <unistd.h>
#include <string.h>
#include <ifaddrs.h>

#define PORT  8910
#define BUFFER_SIZE 1024  

long int unix_timestamp()
{
    time_t t = std::time(0);
    long int now = static_cast<long int> (t);
    return now;
}

int main(int argc, char **argv)  
{
    // 第一个参数是server的IP，第二个参数是client IP 
    if(argc!=3)  
    {  
        printf("usage: client IP \n");  
        exit(0);  
    }  
  
    //定义IPV4的TCP连接的套接字描述符  
    struct sockaddr_in servaddr;  
    memset(&servaddr, 0, sizeof(servaddr));  
    servaddr.sin_family = AF_INET;  
    servaddr.sin_addr.s_addr = inet_addr(argv[1]);  
    servaddr.sin_port = htons(PORT);  //服务器端口  

  
    char sendbuf[BUFFER_SIZE];  
    char recvbuf[BUFFER_SIZE];  
    //客户端将控制台输入的信息发送给服务器端，服务器原样返回信息  
    int county= 1;// 用于计数，一共发送4次
    int ii=1;

    while (1)  
    {  
        //连接服务器，成功返回0，错误返回-1  
        int sock_cli = socket(AF_INET,SOCK_STREAM, 0);  
        if (connect(sock_cli, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)  
        {  
            perror("connect");  
            exit(1);  
        }  
        printf("connect server(IP:%s).\n",argv[1]);  

        if (county==5)//为了让server端退出.
        { 
            sprintf(sendbuf,"exit");//sprintf将格式化的数据写入字符串
        }
        if(county<5)
        {
            sprintf(sendbuf,"send hello%d", county);
        }
        
        std::cerr<<"\n"<<std::endl;        
        std::cerr<<"client发送" << county <<std::endl;
        std::cerr<<sendbuf<<std::endl;
        std::cerr<<"\n"<<std::endl;

        auto start = std::chrono::high_resolution_clock::now();
        send(sock_cli, sendbuf, strlen(sendbuf),0); ///发送  

        if(strcmp(sendbuf,"exit")==0)  
        {   
            printf("\n");  
            printf("client端退出了 exited.\n");  
            printf("\n");  
            break;  
        }  
        // memset(sendbuf, 0, sizeof(sendbuf));  

        recv(sock_cli, recvbuf, sizeof(recvbuf),0); ///接收  
        if (strcmp(recvbuf,"hi, server received *\n")==0)  
        {
            std::cerr<<"client收到正确的 "<< county <<std::endl;
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::cerr<<"client receive:\n"<< county <<std::endl;        
        std::cerr<<recvbuf<<std::endl;
        std::cerr<<"\n"<<std::endl;
        
        // std::cerr<<"1"<<std::endl;
        
        memset(recvbuf, 0, sizeof(recvbuf)); 

        // std::cerr<<"2"<<std::endl;

        std::chrono::duration<double> elapsed_seconds = end-start;
        
        // std::cerr<<"3"<<std::endl;

        std::stringstream ss;
        ss.clear();

        // std::cerr<<"4"<<std::endl;
        
        char stt[INET_ADDRSTRLEN];
        ss<<"{\"host\":\"";
        ss<<inet_ntop(AF_INET, &servaddr.sin_addr, stt, sizeof(stt));
        ss<<"\",";

        // std::cerr<<"5"<<std::endl;

        ss<<"\"timestamp\":"; 
        long int now = unix_timestamp();
        ss<<std::to_string(now);
        ss<<",\"num\":";
        
        // std::cerr<<"6"<<std::endl;

        ss<<std::to_string(ii);
        ii=ii+1;
        ss<<",\"entries\":[[";
        ss<<std::to_string(now);
        
        // std::cerr<<"7"<<std::endl;

        ss<<",\"";
        ss<<inet_ntop(AF_INET,  &servaddr.sin_addr, stt, sizeof(stt));
        ss<<"\",";
        ss<<std::to_string(ntohs(servaddr.sin_port));
        ss<<",\"";

        // std::cerr<<argv[2]<<std::endl;

        // std::cerr<<"10"<<std::endl;

        ss<<argv[2];
        ss<<"\",";
        ss<<PORT;
        ss<<",\"tcp\",";
        ss<<"\"tor\",";
        int amm=strlen(sendbuf);
        ss<<std::to_string(amm);
        ss<<",";
        // std::cerr<<"11"<<std::endl;
        memset(sendbuf, 0, sizeof(sendbuf));  

        ss<<std::to_string(elapsed_seconds.count());
        ss<<",0]]}";
        std::string mm ;
        mm.clear();
        mm=ss.str();

        std::cerr<<"\n"<<std::endl;        
        std::cerr<<"client发送json"<<std::endl;
        std::cerr<<mm<<std::endl;
        std::cerr<<"\n"<<std::endl;


        send(sock_cli, mm.c_str(),mm.size(),0); 
        

        county=county+1;

        sleep(3) ;
    }  

    close(sock_cli );  
    return 0;  
}  
