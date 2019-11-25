#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import ConfigParser
import subprocess
import jaydebeapi
import logging
import xml.etree.ElementTree as ET
import commands
import json
from xpinyin import Pinyin
import re
import cx_Oracle
import datetime
import MySQLdb
import math
from download_ftp import upload_ftp



#文件路径
file_dir='/opt/datatom/dana_ftp_api'
time_cfg="/root/.time.cfg"
jarFile='/opt/datatom/dana_ftp_api/libs/inceptor-driver-5.2.0.jar'
log_path='/opt/datatom/dana_ftp_api/log/'
source_log='source.log'
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

# #log日志
log_name = log_path + source_log
EL = logging.FileHandler(log_name, mode='a')
formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
EL.setFormatter(formatter)
elogger = logging.Logger(name='Sourcelog',level=logging.DEBUG)
elogger.addHandler(EL)


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

#连接源数据库获取源数据信息
def source_params(UnitId,notionalpoolingtype):
	try:
		conn = MySQLdb.connect('172.27.148.98', 'detuo', 'DT@pt18cg', 'detuo_base', 3306,charset='utf8')
		#conn = psycopg2.connect(database="postgres", user="stork",password="stork", host="172.26.16.90", port="14103")
		cursor = conn.cursor()
		cursor.execute("select unitname,ftpip,ftpport,ftpusername,ftppasswd from source_info where unitid = '%s' and notionalpoolingtype = '%s'"%(UnitId,notionalpoolingtype))
		rows = cursor.fetchall()
		for row in rows:
			unitname = row[0]
			ftpip = row[1]
			ftpport = row[2]
			ftpusername = row[3]
			ftppasswd=row[4]
		return unitname,ftpip,ftpport,ftpusername,ftppasswd
		cursor.close()
		conn.close()
	except Exception as e:
		s = sys.exc_info()
		pri.error("source ftp connect failed,please check ftp status!")
		return 1

#获取目的端参数
def init(path_name):
	table_conf="/opt/datatom/dana_ftp_api/table_cfg/%s.conf"%path_name
	#os.system("workflow.sh %s"%table_conf)
	if os.path.exists(table_conf):
		conf = MyConfigParser()
		conf.read(table_conf)
		UnitName = conf.get('info','UnitName')
		Ftppath = conf.get('info','Ftppath')
		XinghuanAddress = conf.get('info','XinghuanAddress')
		HttpfsAddress = conf.get('info','HttpfsAddress')
		SourceTableName = conf.get('info','SourceTableName')
		PrimaryKey = conf.get('info','PrimaryKey')
		XinghuanTableName = conf.get('info','XinghuanTableName')
		XinghuanOrcTableName = conf.get('info','XinghuanOrcTableName')
		MappingList = conf.get('info','MappingList')
		XinghuanUsername = "" 
		XinghuanPassword = ""
		ScheduleType = conf.get('info','ScheduleType')
		TargetList = conf.get('info','TargetList')
		Execrate = conf.get('info','Execrate')
		Field = conf.get('info','Field')
		Fields = json.dumps(eval(str(Field)))
		return UnitName,Ftppath,XinghuanAddress,HttpfsAddress,SourceTableName,PrimaryKey,XinghuanTableName,XinghuanOrcTableName,MappingList,XinghuanUsername,XinghuanPassword,ScheduleType,TargetList,Execrate,Fields
	else:
		pri.error("params %s is not exists"%table_conf)
		return 1



#生成etl,python文件
def etl_update(UnitId,path_name,notionalpoolingtype):
	UnitName,Ftppath,XinghuanAddress,HttpfsAddress,SourceTableName,PrimaryKey,XinghuanTableName,XinghuanOrcTableName,MappingList,XinghuanUsername,XinghuanPassword,ScheduleType,TargetList,Execrate,Fields = init(path_name)
	unitname,ftpip,ftpport,ftpusername,ftppasswd = source_params(UnitId,notionalpoolingtype)

	ScheduleType = str(ScheduleType)
	#建表语句字段拼接
	list=[]
	txt=''
	field = sorted(eval(Fields),key=lambda x:x['column_order'])
	for i in field:
		data = i['column_name']+" "+i['column_type']+" comment '"+ i['column_desc']+"',"
		list.append(data)
	for i in list:
		txt+=i		
	xinghuan_txt = txt.rstrip(",")
	#xinghuan_txt = json.dumps(xinghuan_txt)
	xinghuan_orc = txt.rstrip(",")
	print(xinghuan_txt)
	xinghuan_txt = str(xinghuan_txt.decode("unicode_escape"))
	xinghuan_orc = str(xinghuan_orc.decode("unicode_escape"))
	print("++++++++create table txt table %s++++++++"%xinghuan_txt)
	print("++++++++create table orc table %s++++++++"%xinghuan_orc)

	xinghuan_tbname = XinghuanTableName.split('.')[1]
	xinghuan_dbname = XinghuanTableName.split('.')[0]
	xinghuan_orc_tbname = XinghuanOrcTableName.split('.')[1]
	xinghuan_orc_dbname = XinghuanOrcTableName.split('.')[0]
	ip_unit = ftpip.split('.')[2]+'_'+ftpip.split('.')[3]
	httpfs=HttpfsAddress.split('tmp')[0]
	primarykey = PrimaryKey.split(',')[0]
	token=HttpfsAddress.split('guardian_access_token=')[1]
	httpfsmkdir="%stmp/detuo/?op=MKDIRS&permission=777&guardian_access_token=%s"%(httpfs,token)
	httpfsput1="%stmp/detuo/%s_%s.txt?op=CREATE&guardian_access_token=%s"%(httpfs,unitname,SourceTableName,token)
	httpfsput2="%stmp/detuo/%s_%s.txt?op=CREATE&data=true&guardian_access_token=%s"%(httpfs,unitname,SourceTableName,token)
	with open("/opt/datatom/dana_ftp_api/template/datatom_ftp.py",'r') as fdata :
		fdata = fdata.read().replace("${XinghuanAddress}",XinghuanAddress)
		fdata = fdata.replace("${ftpip}",ftpip)
		fdata = fdata.replace("${ftpport}",ftpport)
		fdata = fdata.replace("${ftpusername}",ftpusername)
		fdata = fdata.replace("${ftppasswd}",ftppasswd)
		fdata = fdata.replace("${Path}",path_name)
		fdata = fdata.replace("${Ftppath}",Ftppath)
		fdata = fdata.replace("${SourceTableName}",SourceTableName)
		fdata = fdata.replace("${XinghuanUsername}",XinghuanUsername)
		fdata = fdata.replace("${XinghuanPassword}",XinghuanPassword)
		fdata = fdata.replace("${unitname}",unitname)
		fdata = fdata.replace("${httpfsmkdir}",httpfsmkdir)
		fdata = fdata.replace("${httpfsput1}",httpfsput1)
		fdata = fdata.replace("${httpfsput2}",httpfsput2)
		fdata = fdata.replace("${xinghuan_orc_tbname}",xinghuan_orc_tbname)
		fdata = fdata.replace("${xinghuan_orc_dbname}",xinghuan_orc_dbname)
		fdata = fdata.replace("${xinghuan_tbname}",xinghuan_tbname)
		fdata = fdata.replace("${xinghuan_dbname}",xinghuan_dbname)
		fdata = fdata.replace("${target_field}","("+TargetList+")")
		fdata = fdata.replace("${original_field}",MappingList)
		fdata = fdata.replace("${Execrate}",Execrate)
		fdata = fdata.replace("${PrimaryKey}",primarykey)
		fdata = fdata.replace("${TxtTable}",xinghuan_txt)
		fdata = fdata.replace("${OrcTable}",xinghuan_orc)
	return fdata


def etl_cfg_file(UnitId,path_name,notionalpoolingtype):
	etl_fdata_cfg = etl_update(UnitId,path_name,notionalpoolingtype)
	m = open("/opt/datatom/dana_ftp_api/execute_cfg/%s.py"%(path_name), 'w')
	os.system("> /opt/datatom/dana_ftp_api/execute_cfg/%s.py"%(path_name))
	m.write(etl_fdata_cfg)
	m.close()

if __name__ == '__main__':
	UnitName,Ftppath,XinghuanAddress,HttpfsAddress,SourceTableName,PrimaryKey,XinghuanTableName,XinghuanOrcTableName,MappingList,XinghuanUsername,XinghuanPassword,ScheduleType,TargetList,Execrate,Fields = init('huanbaoju_test1')
	print(Fields,UnitName)
	unitname,ftpip,ftpport,ftpusername,ftppasswd = source_params('765123','ftp')
	print(unitname,ftppasswd,ftpip)
	xinghuan_tbname = XinghuanTableName.split('.')[1]
	xinghuan_dbname = XinghuanTableName.split('.')[0]
	#ip_unit = sourceip.split('.')[2]+'_'+sourceip.split('.')[3]
	#datax_update('765123','huanbaoju_16_87_test_logs_info')
	#datax_cfg_file('765123','huanbaoju_16_87_test_logs_info')
	#datax_all_file('765123','huanbaoju_16_87_test_logs_info')
	#etl_update('765123','huanbaoju_16_87_test_test1')
	etl_cfg_file('765123','huanbaoju_ftp_16_89_12345_THJLXXYS','ftp')
	#etl_all_file('765123','huanbaoju_16_87_test_logs_info')
	#res = upload_ftp('172.26.16.89',21,'detuoftp','detuoftp','/opt/datatom/ftpdata/','base_test1','huanbaoju')
	#print(res)


	#datax_update(UnitId)
	#执行datax脚本
	#os.system("python /opt/datatom/datax/datax/bin/datax.py /opt/datatom/dana_api/execute_cfg/%s_%s_%s_%s.json"%(unitname,ip_unit,source_dbname,source_tbname))
	#filePath="/opt/datatom/script/%s/data/%s_%s"%(unitname.encode('utf-8'),sourcedbname,SourceTableName)
	#etl_update(UnitId)
	#os.system("python /opt/datatom/dana_api/execute_cfg/%s_%s_%s_%s.py"%(unitname,ip_unit,source_dbname,source_tbname))
	#upload(filePath)
