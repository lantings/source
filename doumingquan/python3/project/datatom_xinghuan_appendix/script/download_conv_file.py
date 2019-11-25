#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ftplib import FTP
import os
import time
import datetime
import binascii

#from get_pic_from_unitname import get_table_count

now_time = time.strftime("%Y%m%d",time.localtime())
ftp = FTP()
#文件下载路径
data_unitname_path = "/tmp/pics/"

def connect_ftp(ftpip,ftpport,ftpuser,ftppasswd):
	ftp.connect(host=ftpip, port=ftpport)
	ftp.login(user=ftpuser, passwd=ftppasswd)
	print("login succeed")

def upload_ftp(ftpip,ftpport,ftpuser,ftppasswd,filepath,tablename,unitname):
	connect_ftp(ftpip,ftpport,ftpuser,ftppasswd)
	x = ftp.nlst(filepath)
	lists = []

	for i in range(len(x)):
		print(x[i])
		#pic文件名
		pic = x[i].split("/")[-1]
		#获取原文件时间
		L = list(ftp.sendcmd('MDTM ' + "%s"%x[i]))
		dir_t=L[4]+L[5]+L[6]+L[7]+'-'+L[8]+L[9]+'-'+L[10]+L[11]+' '+L[12]+L[13]+':'+L[14]+L[15]+':'+L[16]+L[17]
		timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
		#文件时间,总是差8小时
		timestamp = int(time.mktime(timeArray))+28800
		#commontime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		timeArray = time.localtime(timestamp)
		commontime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		
		#系统今天时间 2019-11-19的时间戳 
		today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		todays = time.strptime(today,"%Y-%m-%d")
		todaytime = int(time.mktime(todays))
		
		diff = todaytime-timestamp
		print('this is time differ',diff)
		if diff<86400 and diff>0:
        	#新建unitname目录
        		data_unitname = data_unitname_path + unitname
	    		if os.path.exists(data_unitname)==False:
				os.mkdir(data_unitname)
			else:
				print("weibanju dirname is already created")
			
			print('this is 0<diff<86400',filepath+pic)
		#文件下载
        		with open(data_unitname +"/"+pic, "wb") as f:
            			ftp.retrbinary('RETR '+filepath+"/"+pic,f.write)
        		f.close()
		#将文件转换成16进制
			fh =  open(data_unitname +"/"+pic, "rb")
			a=fh.read()
			hexstr = binascii.hexlify(a)
		#将数据放入list
			b={'name':pic,'time':commontime,'binary':hexstr}
			lists.append(b)
			#print("this is 16 jinzhi",hexstr)
		else:
			print('this is diff<0 or diff>86400',filepath+pic)
	strs=''
	for i in lists:
		strs+=i['name']+"\x01"+i['time']+"\x01"+i['binary']+"\n"
	#生成保存数据的文件
	destpath = tablename
	with open(destpath,'wb') as f:
		f.write(strs)
	return strs

if __name__ == '__main__':
	res = upload_ftp('172.26.16.89',21,'detuoftp','detuoftp','/opt/datatom/ftpdata/','base_test1','huanbaoju')
	#print('this is upload_ftp result',len(res))
	#print('this is upload_ftp result',res)

