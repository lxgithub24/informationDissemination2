# coding=utf-8
# import time
# import datetime
import string
import codecs
readfile = codecs.open("read.txt",'r','utf8')
line = readfile.readline()
# # c = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# # print c 
# # print datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") - datetime.timedelta(minutes=12)
# print type((datetime.datetime.now() - datetime.timedelta(minutes=12)).strftime("%Y-%m-%d %H:%M:%S"))
# timeStamp = int(time.mktime(time.strptime((datetime.datetime.now() - datetime.timedelta(minutes=12)).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")))
# print timeStamp
# a = '流向'
# # if a == '流向':
# #     print 1
# print a!='流向'
# a = "a"+'\b'+"b"+'\t'+"c"+'\r'
# print a
while line=='':
    print "@@@@@@@@@@@@@@@@@@@@"
    line = readfile.readline()
