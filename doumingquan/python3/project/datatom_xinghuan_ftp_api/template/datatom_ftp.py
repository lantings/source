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
#import psycopg2
import datetime
from dateutil.relativedelta import relativedelta
import re
import time
sys.path.append('/opt/datatom/dana_ftp_api/script')
from download_ftp import upload_ftp
from get_bucket_num import get_file_bucket_num
from sftp_xml import analyse_xml


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

#文件路径
file_dir='/opt/datatom/dana_ftp_api/data'
jarFile='/opt/datatom/dana_api/libs/inceptor-driver-5.2.0.jar'
log_path='/opt/datatom/dana_ftp_api/log/'
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
EL = logging.FileHandler(log_name, mode = 'a')
formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
EL.setFormatter(formatter)
elogger = logging.Logger(name = 'Sourcelog',level = logging.DEBUG)
elogger.addHandler(EL)


addtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))[0:8]


def upload():
	file_number = upload_ftp('${ftpip}',${ftpport},'${ftpusername}','${ftppasswd}','${Ftppath}','${SourceTableName}','${unitname}')
	file_number = eval(file_number)
	#获取星环建表桶数
	buckets_num = int(file_number[0]['size'])
	buckets = get_file_bucket_num(buckets_num)
	if file_number[0]['code'] == 1:
		dirver = 'org.apache.hive.jdbc.HiveDriver'
		conn = jaydebeapi.connect(dirver, '${XinghuanAddress}', ['${XinghuanUsername}', '${XinghuanPassword}'], jarFile)
		curs_load = conn.cursor()
		os.system("curl -i -X PUT \"${httpfsmkdir}\"")
		path = "%s/${unitname}/${SourceTableName}"%file_dir
		file_number[0]['filename'].split('_')[0] == 'xml':
			analyse_res = analyse_xml(path,path)
		if analyse_res == False:
			pri.error("xml解析错误！！！")
		for root, dirs, files in os.walk(path):	
			if not os.path.isdir("%s/${SourceTableName}_split"%path):
				os.system("mkdir -p %s/${SourceTableName}_split"%path)
			for i in range(len(files)):
				os.system("split -l 30000000 %s/%s -d -a 10 %s/${SourceTableName}_split/%s"%(path,files[i],path,files[i]))
			break
	#新建txt以及orc表
		curs_txt = conn.cursor()
		if file_number[0]['filename'].split('_')[0] == 'csv': 
			txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable}) STORED AS CSVFILE;"%addtime
			orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable})clustered by (${PrimaryKey}) into %s buckets stored as orc tblproperties('transactional'='true');"%(addtime,buckets)
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")

		elif file_number[0]['filename'].split('_')[0] == 'txt':
			txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable}) ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%addtime
			orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable})clustered by (${PrimaryKey}) into %s buckets stored as orc tblproperties('transactional'='true');"%(addtime,buckets)
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")

		elif file_number[0]['filename'].split('_')[0] == 'xml':
			txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable}) ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%addtime
			orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable})clustered by (${PrimaryKey}) into %s buckets stored as orc tblproperties('transactional'='true');"%(addtime,buckets)
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")

		else:
			pri.error('file type is not support')

		#上传文件并加载到星环
		for file1,file2,file3 in os.walk("%s/${SourceTableName}_split"%path):
			i = 0
			for i in range(len(file3)):
				pri.info("data uploading %s..............."%file3[i])
				os.system("curl -i -X PUT \"${httpfsput1}\"")
				#-C表示支持断点续传
				status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${SourceTableName}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				time.sleep(5)
				print("status=",status)
				count = 1
				while (status != 0 and count <= 5):
					print("file %s upload failed,re-uploading!"%file3[i])
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${SourceTableName}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					count = count + 1
				sqlStr = "load data inpath '/tmp/detuo/${unitname}_${SourceTableName}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%addtime
				curs_load.execute(sqlStr)
			break
		pri.ok("data upload to hdfs succeed")
		curs_insertorc = conn.cursor()	
		#加载数据到事务表
		Execrate = '${Execrate}'
		Execrate = str(Execrate)
		if Execrate == '2':
			pri.info("Full data extraction per day!")
			curs_truncateorc = conn.cursor()
			sql_truncate_orc = "truncate table ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}"
			curs_truncateorc.execute(sql_truncate_orc)
			pri.ok("truncate orc table ${xinghuan_orc_dbname}.${xinghuan_orc_tbname} succeed")
			curs_truncateorc.close()
		else:
			pri.info("incremental data extraction per day!")
		sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s ${target_field} select ${original_field}  from ${xinghuan_dbname}.${xinghuan_tbname}_%s"%(addtime,addtime)
		curs_insertorc.execute(sql_orc)
		pri.ok("insert orc table from txt table succeed!")	
		curs_truncate = conn.cursor()
		sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%addtime
		curs_truncate.execute(sql_truncate)
		pri.ok("truncate txt table ${xinghuan_dbname}.${xinghuan_tbname}_%s succeed!"%addtime)
		curs_load.close()
		curs_insertorc.close()
		curs_truncate.close()
		conn.close()
		pri.ok("table ${SourceTableName}_%s extracte succeed!"%addtime)
		os.system("rm -rf %s"%path)
		curs_txt.close()
	else:
		print("ftp files is not exists")

        
if __name__ == '__main__':
	upload()
