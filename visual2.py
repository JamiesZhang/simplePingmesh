#!/usr/bin/env python
# read data from MySQL and draw heatmap
from pandas import DataFrame
import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
from collections import defaultdict
import MySQLdb

pinglist = open('pinglist.txt')
count = 0
for ping in pinglist:
    count += 1
print 'There are {0} servers.'.format(str(count)) 

pingNum = count * (count-1)

TIME = []
NUM = []
SERVER = []
SERVERPORT = []
CLIENT = []
CLIENTPORT = []
RTT = []

db = MySQLdb.connect("localhost", "root", "zjh123", "PINGMESH", charset='utf8')  # zjh is username, zjh123 is pwd, PINGMESH is database name

cursor = db.cursor()

dictJsonData = {} # record data of each row
for n in range(1, pingNum+1):
    jsonTemp = []
    
    TIME.append([])
    NUM.append([])
    SERVER.append([])
    SERVERPORT.append([])
    CLIENT.append([])
    CLIENTPORT.append([])
    RTT.append([])

    select = "SELECT * FROM table{0}".format(n)
    try:
        cursor.execute(select)
        # get all data of each row
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
print TIME
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

plt.figure("slice"+str(sli)+"-pingmesh")
# ax = plt.subplot(2,1,1)
# Custom palette, you need to pass this parameter cmap into the cmap parameter of the heatmap, see detail: https://www.cntofu.com/book/172/docs/57.md
# cmap=sns.diverging_palette(148, 0, s=75, l=65, n=20, center='light', as_cmap=True)  
pic = sns.heatmap(b, vmin=0, vmax=100, center=20, cmap='YlGnBu', annot=True,  linewidths=1.5,linecolor='white', annot_kws={"size": 7})

# The following action is to highlight the outliers, when RTT>50, the font will be bold
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
