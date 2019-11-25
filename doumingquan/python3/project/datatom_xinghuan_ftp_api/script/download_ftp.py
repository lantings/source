#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from ftplib import FTP
import re
import os
import json
import math
import time
import datetime
now_time = time.strftime("%Y%m%d",time.localtime())
ftp = FTP()
data_unitname_path = "/opt/datatom/dana_ftp_api/data/"
md5_file_path = "/opt/datatom/dana_ftp_api/history_data/"


def connect_ftp(ftpip,ftpport,ftpuser,ftppasswd):
	ftp.connect(host=ftpip, port=ftpport)
	ftp.login(user=ftpuser, passwd=ftppasswd)
	print("login succeed")

def upload_ftp(ftpip,ftpport,ftpuser,ftppasswd,filepath,tablename,unitname):
	connect_ftp(ftpip,ftpport,ftpuser,ftppasswd)
	x = ftp.nlst(filepath)
	lists = []
	for i in range(len(x)):
		#b = r"(txt|csv|xml)_%s_[0-9]{8}(\.([a-zA-Z]{3}))*"%tablename
		b = r"(txt|csv|xml)_%s_[0-9]{8}(\.([a-zA-Z]{3}))?(.md5)?"%tablename
		re_match = re.match(b,x[i].split("/")[-1])
		if re_match:
			print("file is match .... loading this file")
			#检查我们要创建的委办局目录是否存在
			data_unitname = data_unitname_path+unitname
			if os.path.exists(data_unitname)==False:
				os.mkdir(data_unitname)
			else:
				print("weibanju dirname is already created")
			#创建委办局下一级目录(数据库名+表名)
			dirname_data = data_unitname+"/"+tablename
			#检查我们要创建的委办局目录下的 数据库_表 目录是否存在
			if os.path.exists(dirname_data)==False:
			 	os.mkdir(dirname_data)
			else:
				print("db_tablename  dirname is already created")	
			re_group = re_match.group()
			#将文件下载到指定文件夹
			print(dirname_data+"/"+re_group)
			list_set = set(x)
			all = filepath+re_group
			print(list_set,all)
			if all in list_set:
				with open(dirname_data+"/"+re_group,"wb") as f:
					ftp.retrbinary('RETR '+filepath+"/"+re_group,f.write)
					ftp.delete(filepath+"/"+re_group)
				f.close()
				lists.append(re_group)
			else:
				print("file re_match file is not exit")	
		else:
			print("searching files........not match")
	ftp.quit()
	lst = list(set(lists))
	length = len(lst)
	if length==0:
		rests = {"code":0,"result":"没有下载到文件"}
		rst = []
		rst.append(rests)
	else:
		rst = []
		result = {}

	    #创建委办局  /opt/datatom/dana_ftp_api/history_data/
		history_unitname=md5_file_path+unitname                
	    #检查unitname文件是否存在
		if os.path.exists(history_unitname)==False:
			os.mkdir(history_unitname)
		history_data = history_unitname+"/"+tablename+"_"+now_time

		if os.path.exists(history_data)==False:
			os.mkdir(history_data)

		for i in lst:		
			size = os.path.getsize(dirname_data+"/"+i)	
			rests = {"code":1,"size":size,"filename":i,"dirname":dirname_data}
			rst.append(rests)
			os.system("cp %s %s"%(dirname_data+"/"+i,history_data+"/"))
		#print("this is rst--------",rst)
	res = json.dumps(rst)
	return res	


if __name__ == '__main__':
	res = upload_ftp('172.26.16.89',21,'detuoftp','detuoftp','/opt/datatom/ftpdata/','base_test1','huanbaoju')
	print(res)
	#file_type("/tmp/mingquan/","base_test1_2019.txt")





