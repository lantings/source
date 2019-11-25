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
	file_number = upload_ftp('172.26.16.89',21,'detuoftp','detuoftp','/opt/datatom/ftpdata/','test1','huanbaoju')
	file_number = eval(file_number)
	#获取星环建表桶数
	buckets_num = int(file_number[0]['size'])
	buckets = get_file_bucket_num(buckets_num)
	if file_number[0]['code'] == 1:
		dirver = 'org.apache.hive.jdbc.HiveDriver'
		conn = jaydebeapi.connect(dirver, 'jdbc:hive2://172.26.41.32:30366/tdt;guardianToken=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH', ['', ''], jarFile)
		curs_load = conn.cursor()
		os.system("curl -i -X PUT \"http://172.26.41.32:32055/webhdfs/v1/tmp/detuo/?op=MKDIRS&permission=777&guardian_access_token=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH\"")
		path = "%s/huanbaoju/test1"%file_dir
		for root, dirs, files in os.walk(path):	
			if not os.path.isdir("%s/test1_split"%path):
				os.system("mkdir -p %s/test1_split"%path)
			for i in range(len(files)):
				os.system("split -l 30000000 %s/%s -d -a 10 %s/test1_split/%s"%(path,files[i],path,files[i]))
			break
	#新建txt以及orc表
		curs_txt = conn.cursor()
		if file_number[0]['filename'].split('_')[0] == 'csv': 
			txt_table = "create table if not exists tdt.test2_%s(jhpt_update_time varchar(100) comment '数据生成时间',jhpt_time varchar(100) comment '数据时间') STORED AS CSVFILE;"%addtime
			orc_table = "create table if not exists tdt.test3_%s(jhpt_update_time varchar(100) comment '数据生成时间',jhpt_time varchar(100) comment '数据时间')clustered by (JHPT_UPDATE_TIME) into %s buckets stored as orc tblproperties('transactional'='true');"%(addtime,buckets)
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")

		elif file_number[0]['filename'].split('_')[0] == 'txt':
			txt_table = "create table if not exists tdt.test2_%s(jhpt_update_time varchar(100) comment '数据生成时间',jhpt_time varchar(100) comment '数据时间') ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%addtime
			orc_table = "create table if not exists tdt.test3_%s(jhpt_update_time varchar(100) comment '数据生成时间',jhpt_time varchar(100) comment '数据时间')clustered by (JHPT_UPDATE_TIME) into %s buckets stored as orc tblproperties('transactional'='true');"%(addtime,buckets)
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")

		elif file_number[0]['filename'].split('_')[0] == 'xml':
			txt_table = "create table if not exists tdt.test2_%s(jhpt_update_time varchar(100) comment '数据生成时间',jhpt_time varchar(100) comment '数据时间') ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%addtime
			orc_table = "create table if not exists tdt.test3_%s(jhpt_update_time varchar(100) comment '数据生成时间',jhpt_time varchar(100) comment '数据时间')clustered by (JHPT_UPDATE_TIME) into %s buckets stored as orc tblproperties('transactional'='true');"%(addtime,buckets)
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")

		else:
			pri.error('file type is not support')

		#上传文件并加载到星环
		for file1,file2,file3 in os.walk("%s/test1_split"%path):
			i = 0
			for i in range(len(file3)):
				pri.info("data uploading %s..............."%file3[i])
				os.system("curl -i -X PUT \"http://172.26.41.32:32055/webhdfs/v1/tmp/detuo/huanbaoju_test1.txt?op=CREATE&guardian_access_token=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH\"")
				#-C表示支持断点续传
				status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/test1_split/%s \"http://172.26.41.32:32055/webhdfs/v1/tmp/detuo/huanbaoju_test1.txt?op=CREATE&data=true&guardian_access_token=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				time.sleep(5)
				print("status=",status)
				count = 1
				while (status != 0 and count <= 5):
					print("file %s upload failed,re-uploading!"%file3[i])
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/test1_split/%s \"http://172.26.41.32:32055/webhdfs/v1/tmp/detuo/huanbaoju_test1.txt?op=CREATE&data=true&guardian_access_token=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					count = count + 1
				sqlStr = "load data inpath '/tmp/detuo/huanbaoju_test1.txt' into table tdt.test2_%s"%addtime
				curs_load.execute(sqlStr)
			break
		pri.ok("data upload to hdfs succeed")
		curs_insertorc = conn.cursor()	
		#加载数据到事务表
		Execrate = '1'
		Execrate = str(Execrate)
		if Execrate == '2':
			pri.info("Full data extraction per day!")
			curs_truncateorc = conn.cursor()
			sql_truncate_orc = "truncate table tdt.test3"
			curs_truncateorc.execute(sql_truncate_orc)
			pri.ok("truncate orc table tdt.test3 succeed")
			curs_truncateorc.close()
		else:
			pri.info("incremental data extraction per day!")
		sql_orc = "insert into tdt.test3_%s (JHPT_UPDATE_TIME) select JHPT_UPDATE_TIME  from tdt.test2_%s"%(addtime,addtime)
		curs_insertorc.execute(sql_orc)
		pri.ok("insert orc table from txt table succeed!")	
		curs_truncate = conn.cursor()
		sql_truncate = "truncate table tdt.test2_%s"%addtime
		curs_truncate.execute(sql_truncate)
		pri.ok("truncate txt table tdt.test2_%s succeed!"%addtime)
		curs_load.close()
		curs_insertorc.close()
		curs_truncate.close()
		conn.close()
		pri.ok("table test1_%s extracte succeed!"%addtime)
		os.system("rm -rf %s"%path)
		curs_txt.close()
	else:
		print("ftp files is not exists")

        
if __name__ == '__main__':
	upload()
