#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import paramiko
import logging
import os
import xml.etree.ElementTree as ET
import sys
import ConfigParser
import commands
from db import OperDb
import datetime
import time
import jaydebeapi

reload(sys)  
sys.setdefaultencoding('utf8') 

script_path = '/opt/detuo/xml/script'
log_path = '/opt/detuo/xml/log/'
source_log = 'xml.log'
jarFile='/opt/detuo/dana_api/libs/inceptor-driver-5.2.0.jar'
history_xml = '/opt/detuo/xml/history_data'

#定义打印信息类
class Print:
    def info(self, info):
        print('\033[1;36;10m[INFO]%s\033[0m' % info)
    def error(self, error):
        print('\033[1;31;10m[ERROR]%s\033[0m' % error)
        sys.exit(2)
    def ok(self, ok):
        print('\033[1;32;10m[INFO]%s\033[0m' % ok)
pri = Print();


class MyConfigParser(ConfigParser.ConfigParser):
        def __init__(self, defaults=None):
            ConfigParser.ConfigParser.__init__(self, defaults=defaults)
        def optionxform(self, optionstr):
            return optionstr

#log日志
log_name = log_path + source_log
EL = logging.FileHandler(log_name, mode='a')
formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
EL.setFormatter(formatter)
elogger = logging.Logger(name='Sourcelog',level=logging.DEBUG)
elogger.addHandler(EL)



#获取目的端参数
def init():
	table_conf="/opt/detuo/xml/conf/info.cfg"
	if os.path.exists(table_conf):
		conf = MyConfigParser()
		conf.read(table_conf)
		SftpAddress = conf.get('info','SftpAddress')
		SftpPort = conf.get('info','SftpPort')
		SftpUsername =conf.get('info','SftpUsername')
		SftpPassword = conf.get('info','SftpPassword')
		XinghuanUsername = "" 
		XinghuanPassword = ""
		LocalXmlPath = conf.get('info','LocalXmlPath')
		RemoteXmlPath = conf.get('info','RemoteXmlPath')
		TxtPath = conf.get('info','TxtPath')
		XinghuanAddres = conf.get('info','XinghuanAddres')
		HttpfsAddress = conf.get('info','HttpfsAddress')
		UnitName = conf.get('info','UnitName')
		TableName = conf.get('info','TableName')
		return SftpAddress,SftpPort,SftpUsername,SftpPassword,XinghuanUsername,XinghuanPassword,LocalXmlPath,RemoteXmlPath,TxtPath,XinghuanAddres,HttpfsAddress,UnitName,TableName
	else:
		pri.error("params %s is not exists"%table_conf)
		return 1

#连接sftp服务器
def sftp_xml(SftpAddress,SftpPort,SftpUsername,SftpPassword):
#	sf = paramiko.Transport('172.26.41.27', 28)
	sf = paramiko.Transport(SftpAddress, SftpPort)
	sf.connect(username=SftpUsername, password=SftpPassword)
	sftp = paramiko.SFTPClient.from_transport(sf)
	print("conn succeed")
	return sftp 
	sf.close()

#下载文件到本地
def sftp_download(sftp,LocalXmlPath,RemoteXmlPath):
	try:
		if os.path.isdir(LocalXmlPath):
			for f in sftp.listdir(RemoteXmlPath):
				print("fffffffffffff=",f)
				sftp.get(os.path.join(RemoteXmlPath+f),os.path.join(LocalXmlPath+f))
				#sftp.remove(RemoteXmlPath+f)
		else:
			sftp.get(RemoteXmlPath,LocalXmlPath)
	except Exception,e:
		print('download exception:',e)

#解析xml文件
def analyse_xml(LocalXmlPath,TxtPath,TableName):
	for root, dirs, files in os.walk(LocalXmlPath):
		for i in range(len(files)):
			print("111111111",files[i])
			start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		#	xmlFilePath = os.path.abspath("%s%s"%(LocalXmlPath,files[i]))
		#	os.system("cd %s && %s/mkfile.sh"%(history_xml,script_path))
		#	file_name = datetime.datetime.now().strftime('%Y%m%d')
			#print(file_name)
		#	st,out = commands.getstatusoutput("cp %s %s/%s"%(xmlFilePath,history_xml,file_name))
		#	if st == 0:
		#		pri.ok("source xml keep ok")
		#	else:
		#		os.system("mv %s/%s %s/%s_%s"%(history_xml,files[i],history_xml,files[i],time_name))
			status,out = commands.getstatusoutput("cd %s && tail -c 24 %s"%(LocalXmlPath,files[i]))
			xmlFilePath = os.path.abspath("%s%s"%(LocalXmlPath,files[i]))
			if out == '</information></Request>':
				tree = ET.parse(xmlFilePath)
				root = tree.getroot()
				for child in root:
					each_list = []
					for children in child:
						each_list.append(children.text.strip() if children.text else '')
						each_line = '\x01'.join(each_list)
					#print(each_line)
					with open('%s/%s.txt'%(TxtPath,files[i]),'a+') as res:
						res.write(each_line+'\n')
				end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				count_txt = commands.getoutput("wc -l %s/%s.txt  | awk -F ' ' '{print $1}'"%(TxtPath,files[i]))
				time_consuming = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
				results = {}
				results['workflowname'] = files[i]
				results['starttimw'] = start_time
				results['endtime'] = end_time
				results['time_consuming'] = str(time_consuming.seconds)
				results['totallines'] = str(count_txt)
				#results['xhtable'] = XinghuanOrcTableName
				print(type(results))
				print(results)
				if results.has_key("totallines"):
					dbopen = OperDb()
					dbopen.insert_sql(TableName,results)
				else:
					logging.error("analyse xml file failed!")
				status,output = commands.getstatusoutput("rm -f %s"%files[i])
				if status == 0:
					pri.ok("delete %s success"%files[i])
				else:
					pri.error("delete %s failed, please delete it Manual"%files[i])
			else:
				elogger.error("xml file %s is error!"%files[i])
	

		#	tree = ET.parse(xmlFilePath)
			#print ("tree type:", type(tree))
    # 获得根节点
		#	root = tree.getroot()
			#print(root)
		#	for neighbor in root.iter('neighbor'):
		#		print neighbor.attrib
		#	for child in root:
		#		each_list = []
		#		for children in child:
		#			each_list.append(children.text.strip() if children.text else '')
		#			each_line = '\x01'.join(each_list)
					#print(each_line)
		#		with open('%s/%s.txt'%(TxtPath,files[i]),'a+') as res:
		#			res.write(each_line+'\n')
		#	end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		#	count_txt = commands.getoutput("wc -l %s/%s.txt  | awk -F ' ' '{print $1}'"%(TxtPath,files[i]))
		#	time_consuming = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
		#	results = {}
		#	results['workflowname'] = files[i]
		#	results['starttimw'] = start_time
		#	results['endtime'] = end_time
		#	results['time_consuming'] = str(time_consuming.seconds)
		#	results['totallines'] = str(count_txt)
		#	#results['xhtable'] = XinghuanOrcTableName
		#	print(type(results))
		#	print(results)
		#	if results.has_key("totallines"):
		#		dbopen = OperDb()
		#		dbopen.insert_sql(TableName,results)
		#	else:
		#		logging.error("analyse xml file failed!")
		#	status,output = commands.getstatusoutput("rm -f %s"%xmlFilePath)
		#	if status == 0:
		#		pri.ok("delete %s success"%xmlFilePath)
		#	else:
		#		pri.waring("delete %s failed, please delete it Manual"%xmlFilePath)

#抽取到星环

def upload(TxtPath,XinghuanUsername,XinghuanPassword,XinghuanAddres,HttpfsAddress,UnitName):
	try:
		httpfs=HttpfsAddress.split('?')[0]
		print(httpfs)
		token=HttpfsAddress.split('guardian_access_token=')[1]
		print(token)
		httpfsmkdir="%sdetuo/?op=MKDIRS&permission=777&guardian_access_token=%s"%(httpfs,token)
		print(httpfsmkdir)
		dirver = 'org.apache.hive.jdbc.HiveDriver'
		conn = jaydebeapi.connect(dirver, XinghuanAddres, ['', ''], jarFile)
		curs = conn.cursor()
		os.system("curl -i -X PUT \"%s\""%httpfsmkdir)
		#上传文件并加载到星环
		for file1,file2,file3 in os.walk(TxtPath):
			for i in range(len(file3)):
				XinghuanTxtTableName = UnitName+'_'+'txt'+'.'+'ods_'+file3[i].split('_')[0]+'_'+file3[i].split('_')[1]
				XinghuanOrcTableName = UnitName+'_'+'orc'+'.'+'ods_'+file3[i].split('_')[0]+'_'+file3[i].split('_')[1]
				print(XinghuanTxtTableName)
				print(XinghuanOrcTableName)
				httpfsput1 = "%sdetuo/%s?op=CREATE&guardian_access_token=%s"%(httpfs,file3[i],token)
				print(httpfsput1)
				httpfsput2 = "%sdetuo/%s?op=CREATE&data=true&guardian_access_token=%s"%(httpfs,file3[i],token)
				print(httpfsput2)
				os.system("curl -i -X PUT \"%s\""%httpfsput1)
				#-C表示支持断点续传
				status,out = commands.getstatusoutput("curl -i -C - -X PUT -T %s/%s \"%s\" -H \"Content-Type:application/octet-stream\""%(TxtPath,file3[i],httpfsput2))
				time.sleep(5)
				print("status=",status)
				count = 1
				while (status != 0 and count <= 5):
					print("文件%s上传失败,正在重新上传"%file3[i])
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/%s \"%s\" -H \"Content-Type:application/octet-stream\""%(TxtPath,file3[i],httpfsput2))
					count = count + 1
				sqlStr = "load data inpath '/tmp/detuo/%s' into table %s"%(file3[i],XinghuanTxtTableName)
				curs.execute(sqlStr)
				status,output = commands.getstatusoutput("rm -f %s/%s"%(TxtPath,file3[i]))
				if status == 0:
					pri.ok("delete %s/%s success"%(TxtPath,file3[i]))
				else:
					pri.waring("delete %s/%s failed, please delete it Manual"%(TxtPath,file3[i]))
			break
		#curs2 = conn.cursor()	
		#加载数据到事务表
		#sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname} select * from ${xinghuan_dbname}.${xinghuan_tbname}"
		#curs2.execute(sql_orc)	
		#curs3 = conn.cursor()
		#sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}"
		#curs3.execute(sql_truncate)
		curs.close()
		#curs2.close()
		#curs3.close()
		conn.close()
		pri.ok("表%s抽取成功"%xinghuantablename)
	except Exception as e:
		s = sys.exc_info()
    
if __name__ == '__main__':
	SftpAddress,SftpPort,SftpUsername,SftpPassword,XinghuanUsername,XinghuanPassword,LocalXmlPath,RemoteXmlPath,TxtPath,XinghuanAddres,HttpfsAddress,UnitName,TableName = init()
	#sftp = sftp_xml(SftpAddress,SftpPort,SftpUsername,SftpPassword)
	#sftp_download(sftp,LocalXmlPath,RemoteXmlPath)
	#analyse_xml(LocalXmlPath,TxtPath,TableName)
	upload(TxtPath,XinghuanUsername,XinghuanPassword,XinghuanAddres,HttpfsAddress,UnitName)
