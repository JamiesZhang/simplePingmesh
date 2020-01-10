#!/usr/bin/env python
# 从MySQL中读数据
from pandas import DataFrame
import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
from collections import defaultdict
import MYSQLdb

pinglist = open('pinglist.txt')
count = 0
for ping in pinglist:
    count += 1
print 'There are {0} servers.'.format(str(count)) 
# 一共有n个server，两两互ping，有 n*(n-1) 种结果
pingNum = count * (count-1)

TIME = []
NUM = []
SERVER = []
SERVERPORT = []
CLIENT = []
CLIENTPORT = []
RTT = []

# 打开数据库链接
db = MySQLdb.connect("localhost", "zjh", "zjh123", "PINGMESH")  # zjh指登录数据库的用户名， zjh123指密码， PINGMESH是数据库名称

# 使用cursor()方法获取操作游标
cursor = db.cursor()

dictJsonData = {} # 用于记录每一行json数据
for n in range(1, pingNum+1):
    jsonTemp = []
    
    TIME.append([])
    NUM.append([])
    SERVER.append([])
    SERVERPORT.append([])
    CLIENT.append([])
    CLIENTPORT.append([])
    RTT.append([])

    select = "SELECT * FROM {0}".format(n)
    try:
        # 执行sql语句
        cursor.execute(select)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            TIME[n-1].append(row[0])      # timestamp
            NUM[n-1].append(row[1])       # num
            SERVER[n-1].append(row[2])    # serverIP
            SERVERPORT[n-1].append(row[3])# serverPort
            CLIENT[n-1].append(row[4])    # clientIP
            CLIENTPORT[n-1].append(row[5])# clientPort
            RTT[n-1].append(row[6])       # RTT
    except:
        print "Error: unable to fetch data"

sli = int(input("Which time slice do you want to draw:CHOOSE FROM "+str(NUM[0][0])+","+str(NUM[0][count-1])+","+str(NUM[0][2*count-2])+","+str(NUM[0][3*count-3])+":  "))

NEWTIME=[]
NEWSERVER=[]
NEWCLIENT=[]
NEWRTT=[]
for p in range(count):
    for q in range(len(NUM[0])):
        if NUM[p][q] == sli:
            NEWTIME.append(TIME[p][q])
            NEWSERVER.append (SERVER[p][q].split(".")[-1])
            NEWCLIENT.append (CLIENT[p][q].split(".")[-1])
            NEWRTT.append (RTT[p][q]*100000)
# print(" ***********************  ***********************  ***********************  ***********************")
# print("newTIME={}".format(NEWTIME))
# print("newSERVER={}".format(NEWSERVER))
# print("newCLIENT={}".format(NEWCLIENT))
# print("newRTT={}".format(NEWRTT))
# print(" ***********************  ***********************  ***********************  ***********************")

data = {'time':NEWTIME, 'server':NEWSERVER, 'client':NEWCLIENT, 'rtt':NEWRTT}
df = DataFrame(data)
# print(df)
b = df.pivot('server', 'client', 'rtt')
# print(b)

# 下面开始画图
plt.figure("slice"+str(sli)+"-pingmesh") # 这个地方显示在文件名上
# ax = plt.subplot(2,1,1)
# 自定义的调色板，需要将这个参数cmap传入sns.heatmap的cmap参数中，详情见：https://www.cntofu.com/book/172/docs/57.md
# cmap=sns.diverging_palette(148, 0, s=75, l=65, n=20, center='light', as_cmap=True)  
pic = sns.heatmap(b, vmin=0, vmax=100, center=20, cmap='YlGnBu', annot=True,  linewidths=1.5,linecolor='white', annot_kws={"size": 7})

# 下面作用是突出异常值，当 RTT>50 的时候，字体会加大加粗
# for text in pic.texts:
#     text.set_size(7)
#     if int(float(text.get_text())) >int(50):
#         text.set_size(12)
#         text.set_weight('bold')
#         text.set_style('italic')

plt.title('Pingmesh Heatmap (rtt*10^-5)')
plt.xlabel('Server')
plt.ylabel('Client')
plt.show()