#!/usr/bin/env python
from pandas import DataFrame
import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
from collections import defaultdict

pinglist = open('pinglist.txt')
count = 0
for ping in pinglist:
    count += 1
print('There are {0} servers.'.format(str(count)))

# 一共有n个server，两两互ping，有 n*(n-1) 种结果
pingNum = count * (count-1)

RTT = []
SERVER = []
CLIENT = []
TIME = []
NUM = []

dictJsonData = {} # 用于记录每一行json数据
for n in range(1, pingNum+1):
    jsonTemp = []
    with open('./'+"result/"+str(n)+'/result.json') as f: # 打开每一组测试结果的json数据
        try:
            while True:
                fp = f.readline()
                js = json.loads(fp)
                jsonTemp.append(js)
            else:
                break
        except:
            f.close()
            print("the result {0} already done.".format(n))
        for i in range(4*(count-1)): #对于每一行测试数据，也就是每一组的每一个时间片上的测试
            if i==0:
                dictJsonData = dict(jsonTemp[i])
                for j in dictJsonData.items():
                    if j[0] != 'entries':
                        dictJsonData[str(j[0])] = [dictJsonData[str(j[0])]]
                # print("dictJsonData:________________________")
                # print(dictJsonData)
            else:
                for b in jsonTemp[i].items():
                    # print("b={}".format(b))
                    if b[0] != 'entries':
                        dictJsonData[b[0]].append(b[1])
                    else:
                        dictJsonData[b[0]].append(b[1][0])
                # print("dictJsonData2:================")
                # print(dictJsonData)
        TIME.append([])
        SERVER.append([])
        CLIENT.append([])
        RTT.append([])
        NUM.append([])
        for i in dictJsonData['num']:
            print(i)
            NUM[n-1].append(i)
        for jsondict in dictJsonData['entries']:
            TIME[n-1].append(jsondict[0])  # timestamp
            SERVER[n-1].append(jsondict[1])  # server
            CLIENT[n-1].append(jsondict[3])  # client
            RTT[n-1].append(jsondict[-2])  # RTT
        print(" ***********************  ***********************  ***********************  ***********************")
        print("NUN={}".format(NUM))
        print("TIME={}".format(TIME))
        print("SERVER={}".format(SERVER))
        print("CLIENT={}".format(CLIENT))
        print("RTT={}".format(RTT))
        print(" ***********************  ***********************  ***********************  ***********************")

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
print(" ***********************  ***********************  ***********************  ***********************")
print("newTIME={}".format(NEWTIME))
print("newSERVER={}".format(NEWSERVER))
print("newCLIENT={}".format(NEWCLIENT))
print("newRTT={}".format(NEWRTT))
print(" ***********************  ***********************  ***********************  ***********************")

data = {'time':NEWTIME, 'server':NEWSERVER, 'client':NEWCLIENT, 'rtt':NEWRTT}
df = DataFrame(data)
print(df)
b = df.pivot('server', 'client', 'rtt')
print(b)

# 下面开始画图
plt.figure("slice"+str(sli)+"-pingmesh") # 这个地方显示在文件名上
# plt.figure()
# ax = plt.subplot(2,1,1)
# cc=sns.diverging_palette(148, 0, s=75, l=65, n=20, center='light', as_cmap=True)
pic = sns.heatmap(b, vmin=0, vmax=100, center=20, cmap='YlGnBu', annot=True,  linewidths=1.5,linecolor='white', annot_kws={"size": 7})
# for text in pic.texts:
#     text.set_size(7)
#     if int(float(text.get_text())) >int(50):
#         text.set_size(12)
#         text.set_weight('bold')
#         text.set_style('italic')
# sns.show()
plt.title('Pingmesh Heatmap (rtt*10^-5)')
plt.xlabel('Server')
plt.ylabel('Client')
plt.show()