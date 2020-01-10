#!/usr/bin/env python
# Save data to MySQL
import MySQLdb
import os
import json

# before this, we need to build a database named 'PINGMESH' under user 'zjh'
# open the connection of database
db = MySQLdb.connect("localhost", "zjh", "zjh123", "PINGMESH", charset='utf8')  # zjh is username， zjh123 is pwd， PINGMESH is database name

# use cursor() get cursor
cursor = db.cursor()

count = len(os.listdir("result"))  # 'count' test
# create a table for each test
for n in os.listdir("result"):
    # create table
    create = """CREATE TABLE {0} (
         timestamp  BIGINT NOT NULL,
         num        INT,
         serverIP   CHAR(36),
         serverPort INT,
         clientIP   CHAR(36),
         clientPort INT,
         RTT        DOUBLE )""".format(n)
    
    cursor.execute(create)

    # read json file of each test 
    jsonTemp = []
    with open('./'+"result/"+str(n)+'/result.json') as f:
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
        for i in range(4):
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
            
            insert = """INSERT INTO {0}(timestamp, num,
                        serverIP, serverPort, clientIP, clientPort, RTT)
                        VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7})""".format(n, timestamp, i, serverIP, serverPort, clientIP, clientPort, RTT)
            try:
                cursor.execute(insert)
                # commit to database and execute
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
db.close()
