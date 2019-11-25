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
import psycopg2
import datetime
import re
import time
sys.path.append('/opt/datatom/dana_api/script')
from check_datax_log import operate_tables

#文件路径
file_dir='/opt/datatom/dana_api/data'
jarFile='/opt/datatom/dana_api/libs/inceptor-driver-5.2.0.jar'
log_path='/opt/datatom/dana_api/log/'
source_log='source.log'


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

#log日志
log_name = log_path + source_log
EL = logging.FileHandler(log_name, mode='a')
formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
EL.setFormatter(formatter)
elogger = logging.Logger(name='Sourcelog',level=logging.DEBUG)
elogger.addHandler(EL)


addtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))[0:8]


#执行datax并把日志写入库
def action_datax():
	try:
		#os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_api/${exec_datax}/${Path}.json > /opt/datatom/dana_api/log/${exec_datax_log}/${Path}.log"%addtime)
		os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_api/${exec_datax}/${Path}.json > /opt/datatom/dana_api/log/${Path}.log"%addtime)
		operate_tables('/opt/datatom/dana_api/log/${Path}.log', '${xinghuan_dbname}.${xinghuan_tbname}', '${source_dbname}.${source_tbname}','public.job_run_info')
		pri.ok("table ${source_dbname}.${source_tbname} data extraction txt succeed，uploading to inceptor!")
	except Exception as e:
		s = sys.exc_info()


def upload():
	try:
		dirver = 'org.apache.hive.jdbc.HiveDriver'
		conn = jaydebeapi.connect(dirver, '${XinghuanAddress}', ['${XinghuanUsername}', '${XinghuanPassword}'], jarFile)
		curs = conn.cursor()
		os.system("curl -i -X PUT \"${httpfsmkdir}\"")
		path="%s/${unitname}/${source_dbname}_${source_tbname}"%file_dir
		for root, dirs, files in os.walk(path):	
			if not os.path.isdir("%s/${source_dbname}_${source_tbname}_split"%path):
				os.system("mkdir -p %s/${source_dbname}_${source_tbname}_split"%path)
			for i in range(len(files)):
				os.system("split -l 5000000 %s/%s -d -a 10 %s/${source_dbname}_${source_tbname}_split/%s"%(path,files[i],path,files[i]))
			break
		#上传文件并加载到星环
		for file1,file2,file3 in os.walk("%s/${source_dbname}_${source_tbname}_split"%path):
			i=0
			for i in range(len(file3)):
				os.system("curl -i -X PUT \"${httpfsput1}\"")
				#-C表示支持断点续传
				#os.system("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				pri.info("data uploading...............")
				status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				time.sleep(5)
				print("status=",status)
				count = 1
				while (status != 0 and count <= 5):
					print("file %s upload failed,re-uploading!"%file3[i])
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					count = count + 1
				sqlStr = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}"
				curs.execute(sqlStr)
			break
		pri.ok("data upload to hdfs succeed")
		curs2 = conn.cursor()	
		#加载数据到事务表
		Execrate = '${Execrate}'
		Execrate = str(Execrate)
		if Execrate == '2':
			pri.info("Full data extraction per day!")
			curs4 = conn.cursor()
			sql_truncate_orc = "truncate table ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}"
			curs4.execute(sql_truncate_orc)
			pri.ok("truncate orc table ${xinghuan_orc_dbname}.${xinghuan_orc_tbname} succeed")
			curs4.close()
		else:
			pri.info("incremental data extraction per day!")
		sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname} ${target_field} select ${original_field}  from ${xinghuan_dbname}.${xinghuan_tbname}"
		curs2.execute(sql_orc)
		pri.ok("insert orc table from txt table succeed!")	
		curs3 = conn.cursor()
		sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}"
		curs3.execute(sql_truncate)
		pri.ok("truncate txt table ${xinghuan_dbname}.${xinghuan_tbname} succeed!")
		curs.close()
		curs2.close()
		curs3.close()
		conn.close()
		pri.ok("table ${source_dbname}.${source_tbname} extracte succeed!")
		os.system("rm -rf  %s"%path)
	except Exception as e:
		s = sys.exc_info()
		

        
if __name__ == '__main__':
	action_datax()
	upload()
