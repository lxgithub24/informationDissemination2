# coding=utf-8
import MySQLdb  
import codecs

#读取爬取到的文件，按照用户名判断是否在数据库中存在，并返回id
infofile = codecs.open("inforead.txt", 'r', 'utf-8')
infofilenew = codecs.open("infowrite.txt", 'a', 'utf-8')
username = infofile.readline()
conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "zijidelu", db = "school", use_unicode=True, charset="utf8")  
cursor = conn.cursor ()  
# cursor.execute('SET NAMES gbk')
while username!="":
    username = username.split(' ')
    givenname = username[0]
    givenname = givenname 
    #判断该用户是否已存在
    cursor.execute ("SELECT id from teacher where name='"+givenname+"'")  
    rows = cursor.fetchall()  
    if len(rows)>0:
        #存在则返回该用户的id
        id = rows[0][0]
    elif len(rows)==0:
        #不存在则插入到数据库
#         print type(givenname)
#         print givenname
#         print type(givenname)
#         print givenname
#         print type('流向1想')
        print givenname=='流想'
        cursor.execute("insert into teacher(name,age,xi) values('"+givenname+"',12,6)")
        conn.commit()  
        cursor.execute ("SELECT id from teacher where name='"+givenname+"'")
        row = cursor.fetchall()
        id = row[0][0]
    print id
    infofilenew.write(str(id)+" "+username[1])
    username = infofile.readline()


cursor.close ()  
conn.close ()  
