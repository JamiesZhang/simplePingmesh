#!/usr/bin/env python
# Save data to MySQL
import MySQLdb
import os
import json

# 在这之前，需要先在用户zjh下建一个PINGMESH的数据库
# 打开数据库链接
db = MySQLdb.connect("localhost", "zjh", "zjh123", "PINGMESH", , charset='utf8')  # zjh指登录数据库的用户名， zjh123指密码， PINGMESH是数据库名称

# 使用cursor()方法获取操作游标
cursor = db.cursor()

count = len(os.listdir("result"))  # 一共有count对测试
# 为每一对测试创建一个数据库表
for n in os.listdir("result"):
    # 创建表
    create = """CREATE TABLE {0} (
         timestamp  BIGINT NOT NULL,
         num        INT,
         serverIP   CHAR(36),
         serverPort INT,
         clientIP   CHAR(36),
         clientPort INT,
         RTT        DOUBLE )""".format(n)
    
    cursor.execute(create)

    # 读取每一对测试中的json文件
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
            print "the result {0} already done.".format(n)
        for i in range(4): #对于每一行测试数据，也就是每一组的每一个时间片上的测试
            if i==0:
                dictJsonData = dict(jsonTemp[i])
                for j in dictJsonData.items():
                    if j[0] != 'entries':
                        dictJsonData[str(j[0])] = [dictJsonData[str(j[0])]]
            else:
                for b in jsonTemp[i].items():
                    # print("b={}".format(b))
                    if b[0] != 'entries':
                        dictJsonData[b[0]].append(b[1])
                    else:
                        dictJsonData[b[0]].append(b[1][0])
        for jsondict, i in dictJsonData['entries'], dictJsonData['num']:
            timestamp = jsondict[0]
            serverIP = jsondict[1]
            serverPort = jsondict[2]
            clientIP = jsondict[3]
            clientPort = jsondict[4]
            RTT = jsondict[-2]
            
            # 向数据库中插入数据
            insert = """INSERT INTO {0}(timestamp, num,
                        serverIP, serverPort, clientIP, clientPort, RTT)
                        VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7})""".format(n, timestamp, i, serverIP, serverPort, clientIP, clientPort, RTT)
            try:
                # 执行sql语句
                cursor.execute(insert)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()

# 关闭数据库链接
db.close()
