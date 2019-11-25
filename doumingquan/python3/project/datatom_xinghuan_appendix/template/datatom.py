#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import ConfigParser
import subprocess
import jaydebeapi
import logging
import shutil
import xml.etree.ElementTree as ET
import commands
#import psycopg2
import datetime
from dateutil.relativedelta import relativedelta
import re
import time
sys.path.append('/opt/datatom/dana_appendix_api/script')
from check_datax_log import operate_tables
from send_datax_log import sed_log


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

#文件路径
file_dir = '/opt/datatom/dana_appendix_api/data'
appendix_dir = '/opt/datatom/dana_appendix_api/data_appendix'
jarFile = '/opt/datatom/dana_appendix_api/libs/inceptor-driver-5.2.0.jar'
log_path = '/opt/datatom/dana_appendix_api/log/'
source_log = 'source.log'


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
day_time = (datetime.datetime.now() + datetime.timedelta(days = -2)).strftime("%Y%m%d%H%M%S")[0:8]
month_time = (datetime.datetime.now() - relativedelta(months = 1)).strftime("%Y%m%d%H%M%S")[0:6]



#执行datax并把日志写入库
def action_datax():
	ScheduleType = '${ScheduleType}'
	if ScheduleType == '1':
		#os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/${exec_datax}/${Path}.json > /opt/datatom/dana_appendix_api/log/${exec_datax_log}/${Path}.log"%addtime)
		os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/${exec_datax}/${Path}.json > /opt/datatom/dana_appendix_api/log/${Path}.log"%addtime)
		#sed_log('${Path}')
		operate_tables('/opt/datatom/dana_appendix_api/log/${Path}.log', '${xinghuan_dbname}.${xinghuan_tbname}_%s'%day_time, '${source_dbname}.${source_tbname}','detuo_base.job_run_info')
		pri.ok("table ${source_dbname}.${source_tbname} data extraction txt succeed，uploading to inceptor!")
	elif ScheduleType == '3':
		#os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/${exec_datax}/${Path}.json > /opt/datatom/dana_appendix_api/log/${exec_datax_log}/${Path}.log"%addtime)
		os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/${exec_datax}/${Path}.json > /opt/datatom/dana_appendix_api/log/${Path}.log"%addtime)
		#sed_log('${Path}')
		operate_tables('/opt/datatom/dana_appendix_api/log/${Path}.log', '${xinghuan_dbname}.${xinghuan_tbname}_%s'%month_time, '${source_dbname}.${source_tbname}','detuo_base.job_run_info')
		pri.ok("table ${source_dbname}.${source_tbname} data extraction txt succeed，uploading to inceptor!")
	else:
		print("ScheduleType is not exists")



def upload():
    #数据库连接
	dirver = 'org.apache.hive.jdbc.HiveDriver'
	conn = jaydebeapi.connect(dirver, '${XinghuanAddress}', ['${XinghuanUsername}', '${XinghuanPassword}'], jarFile)
	curs_load = conn.cursor()
	os.system("curl -i -X PUT \"${httpfsmkdir}\"")
	path = "%s/${unitname}/${source_dbname}_${source_tbname}"%file_dir
	appendix_path = "%s/${unitname}/${source_dbname}_${source_tbname}"%appendix_dir
	#数据切割，防止一次性数据量过大
	for root, dirs, files in os.walk(path):	
		if not os.path.isdir("%s/${source_dbname}_${source_tbname}_split"%path):
			os.system("mkdir -p %s/${source_dbname}_${source_tbname}_split"%path)
		for i in range(len(files)):
			os.system("split -l 5000000 %s/%s -d -a 10 %s/${source_dbname}_${source_tbname}_split/%s"%(path,files[i],path,files[i]))
		break
	curs_txt = conn.cursor()
	ScheduleType = '${ScheduleType}'
	Type = '${Type}'
	#数据归集类型为每天
	if ScheduleType == '1':
		#源库存的是附件本身
		if Type == '1':	
			#新建txt以及orc表
			txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable})ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%day_time
			orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable}) stored as hyperdrive;"%day_time
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")
			#上传文件并加载到星环
			for file1,file2,file3 in os.walk("%s/${source_dbname}_${source_tbname}_split"%path):
				i=0
				for i in range(len(file3)):
					pri.info("data uploading %s..............."%file3[i])
					os.system("curl -i -X PUT \"${httpfsput1}\"")
					#-C表示支持断点续传
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					time.sleep(5)
					print("status=",status)
					count = 1
					while (status != 0 and count <= 5):
						print("file %s upload failed,re-uploading!"%file3[i])
						status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
						count = count + 1
					sqlStr = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%day_time
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
			sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s ${target_field} select ${original_field}  from ${xinghuan_dbname}.${xinghuan_tbname}_%s"%(day_time,day_time)
			curs_insertorc.execute(sql_orc)
			pri.ok("insert orc table from txt table succeed!")	
			curs_truncate = conn.cursor()
			sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%day_time
			curs_truncate.execute(sql_truncate)
			pri.ok("truncate txt table ${xinghuan_dbname}.${xinghuan_tbname}_%s succeed!"%day_time)
			curs_load.close()
			curs_insertorc.close()
			curs_truncate.close()
			conn.close()
			pri.ok("table ${source_dbname}.${source_tbname}_%s extracte succeed!"%day_time)
			shutil.rmtree(path)
			#os.system("rm -rf %s"%path)
		#源库存的是附件路径
		elif Type == '2':
			res = upload_ftp('${ftpip}', ${ftpport}, '${ftpusername}', '${ftppasswd}', '${Ftppath}', '${unitname}','${source_tbname}')
			if res == True:
				#新建txt以及orc表
				txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable})ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%day_time
				orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable}) stored as hyperdrive;"%day_time
				print("xinghuan_txt create table sql:",txt_table)
				print("xinghuan_orc create table sql:",orc_table)
				curs_txt.execute(txt_table)
				curs_txt.execute(orc_table)
				pri.info("---------------------create xinghuan_txt table is success----------------")
				pri.info("---------------------create xinghuan table is success----------------")
				#新建照片表
				txt_zp_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_zp (zpid string, zpsj timestamp, zp blob) ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"
				txt_zp_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_zp (zpid string, zpsj timestamp, zp blob) stored as hyperdrive;"
				curs_txt.execute(txt_table)
				curs_txt.execute(orc_table)
				pri.info("---------------------create xinghuan_txt_zp table is success----------------")
				pri.info("---------------------create xinghuan_zp table is success----------------")
				#上传文件并加载到星环（包含数据库中数据以及附件数据）
				for file1,file2,file3 in os.walk("%s/${source_dbname}_${source_tbname}_split"%path):
					i=0
					for i in range(len(file3)):
						pri.info("data uploading %s..............."%file3[i])
						os.system("curl -i -X PUT \"${httpfsput1}\"")
						#-C表示支持断点续传
						status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
						time.sleep(5)
						print("status=",status)
						count = 1
						while (status != 0 and count <= 5):
							print("file %s upload failed,re-uploading!"%file3[i])
							status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
							count = count + 1
						sqlStr = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%day_time
						curs_load.execute(sqlStr)
					break

				for file1,file2,file3 in os.walk("%s/${unitname}/${source_dbname}_${source_tbname}"%appendix_path):
					i=0
					for i in range(len(file3)):
						pri.info("data uploading %s..............."%file3[i])
						os.system("curl -i -X PUT \"${httpfsput1}\"")
						#-C表示支持断点续传
						status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${unitname}/${source_dbname}_${source_tbname}/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(appendix_path,file3[i]))
						time.sleep(5)
						print("status=",status)
						count = 1
						while (status != 0 and count <= 5):
							print("file %s upload failed,re-uploading!"%file3[i])
							status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${unitname}/${source_dbname}_${source_tbname}/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(appendix_path,file3[i]))
							count = count + 1
						sqlStr_zp = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_zp"
						curs_load.execute(sqlStr_zp)
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
				sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s ${target_field} select ${original_field}  from ${xinghuan_dbname}.${xinghuan_tbname}_%s"%(day_time,day_time)
				sql_orc_zp = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_zp  select * from ${xinghuan_dbname}.${xinghuan_tbname}_zp"
				curs_insertorc.execute(sql_orc)
				curs_insertorc.execute(sql_orc_zp)
				pri.ok("insert orc table from txt table succeed!")	
				curs_truncate = conn.cursor()
				sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%day_time
				sql_truncate_zp = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_zp"
				curs_truncate.execute(sql_truncate)
				curs_truncate.execute(sql_truncate_zp)
				pri.ok("truncate txt table ${xinghuan_dbname}.${xinghuan_tbname}_%s and zp succeed!"%day_time)
				curs_load.close()
				curs_insertorc.close()
				curs_truncate.close()
				conn.close()
				pri.ok("table ${source_dbname}.${source_tbname}_%s extracte succeed!"%day_time)
				shutil.rmtree(path)
				shutil.rmtree(appendix_path)
			else:
				pri.error("appendix download error!!")
		else:
			pri.error("Type is not exists")
    #数据归集类型为每月
	elif ScheduleType == '3':
		if Type == '1':
			txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable})ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%month_time
			orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable})clustered by (${PrimaryKey}) into ${buckets} buckets stored as orc tblproperties('transactional'='true');"%month_time
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")
			for file1,file2,file3 in os.walk("%s/${source_dbname}_${source_tbname}_split"%path):
				i=0
				for i in range(len(file3)):
					pri.info("data uploading %s..............."%file3[i])
					os.system("curl -i -X PUT \"${httpfsput1}\"")
					#-C表示支持断点续传
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					time.sleep(5)
					print("status=",status)
					count = 1
					while (status != 0 and count <= 5):
						print("file %s upload failed,re-uploading!"%file3[i])
						status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${source_dbname}_${source_tbname}_split/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
						count = count + 1
					sqlStr = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%month_time
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
			sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s ${target_field} select ${original_field}  from ${xinghuan_dbname}.${xinghuan_tbname}_%s"%(month_time,month_time)
			curs_insertorc.execute(sql_orc)
			pri.ok("insert orc table from txt table succeed!")	
			curs_truncate = conn.cursor()
			sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%month_time
			curs_truncate.execute(sql_truncate)
			pri.ok("truncate txt table ${xinghuan_dbname}.${xinghuan_tbname}_%s succeed!"%month_time)
			curs_load.close()
			curs_insertorc.close()
			curs_truncate.close()
			conn.close()
			pri.ok("table ${source_dbname}.${source_tbname}_%s extracte succeed!"%month_time)
			shutil.rmtree(path)
		#源库存的是附件路径
		elif Type == '2':
			res = upload_ftp('${ftpip}', ${ftpport}, '${ftpusername}', '${ftppasswd}', '${Ftppath}', '${unitname}','${source_tbname}')
			if res == True:
				#新建txt以及orc表
				txt_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_%s(${TxtTable})ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%month_time
				orc_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s(${OrcTable}) stored as hyperdrive;"%month_time
				print("xinghuan_txt create table sql:",txt_table)
				print("xinghuan_orc create table sql:",orc_table)
				curs_txt.execute(txt_table)
				curs_txt.execute(orc_table)
				pri.info("---------------------create xinghuan_txt table is success----------------")
				pri.info("---------------------create xinghuan table is success----------------")
				#新建照片表
				txt_zp_table = "create table if not exists ${xinghuan_dbname}.${xinghuan_tbname}_zp (zpid string, zpsj timestamp, zp blob) ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"
				txt_zp_table = "create table if not exists ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_zp (zpid string, zpsj timestamp, zp blob) stored as hyperdrive;"
				curs_txt.execute(txt_table)
				curs_txt.execute(orc_table)
				pri.info("---------------------create xinghuan_txt_zp table is success----------------")
				pri.info("---------------------create xinghuan_zp table is success----------------")
				#上传文件并加载到星环
				for file1,file2,file3 in os.walk("%s/${unitname}/${source_dbname}_${source_tbname}"%path):
					i=0
					for i in range(len(file3)):
						pri.info("data uploading %s..............."%file3[i])
						os.system("curl -i -X PUT \"${httpfsput1}\"")
						#-C表示支持断点续传
						status,out = commands.getstatusoutput("curl -i -C - -X PUT -T %s/${unitname}/${source_dbname}_${source_tbname}/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
						time.sleep(5)
						print("status=",status)
						count = 1
						while (status != 0 and count <= 5):
							print("file %s upload failed,re-uploading!"%file3[i])
							status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${unitname}/${source_dbname}_${source_tbname}/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
							count = count + 1
						sqlStr = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%month_time
						curs_load.execute(sqlStr)
					break
				for file1,file2,file3 in os.walk("%s/${unitname}/${source_dbname}_${source_tbname}"%appendix_path):
					i=0
					for i in range(len(file3)):
						pri.info("data uploading %s..............."%file3[i])
						os.system("curl -i -X PUT \"${httpfsput1}\"")
						#-C表示支持断点续传
						status,out = commands.getstatusoutput("curl -i -C - -X PUT -T %s/${unitname}/${source_dbname}_${source_tbname}/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(appendix_path,file3[i]))
						time.sleep(5)
						print("status=",status)
						count = 1
						while (status != 0 and count <= 5):
							print("file %s upload failed,re-uploading!"%file3[i])
							status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/${unitname}/${source_dbname}_${source_tbname}/%s \"${httpfsput2}\" -H \"Content-Type:application/octet-stream\""%(appendix_path,file3[i]))
							count = count + 1
						sqlStr_zp = "load data inpath '/tmp/detuo/${unitname}_${source_dbname}_${source_tbname}.txt' into table ${xinghuan_dbname}.${xinghuan_tbname}_zp"
						curs_load.execute(sqlStr_zp)
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
				sql_orc = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_%s ${target_field} select ${original_field}  from ${xinghuan_dbname}.${xinghuan_tbname}_%s"%(month_time,month_time)
				sql_orc_zp = "insert into ${xinghuan_orc_dbname}.${xinghuan_orc_tbname}_zp select * from ${xinghuan_dbname}.${xinghuan_tbname}_zp"
				curs_insertorc.execute(sql_orc)
				curs_insertorc.execute(sql_orc_zp)
				pri.ok("insert orc table from txt table succeed!")	
				curs_truncate = conn.cursor()
				sql_truncate = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_%s"%month_time
				sql_truncate_zp = "truncate table ${xinghuan_dbname}.${xinghuan_tbname}_zp"
				curs_truncate.execute(sql_truncate)
				curs_truncate.execute(sql_truncate_zp)
				pri.ok("truncate txt table ${xinghuan_dbname}.${xinghuan_tbname}_%s succeed!"%month_time)
				curs_load.close()
				curs_insertorc.close()
				curs_truncate.close()
				conn.close()
				pri.ok("table ${source_dbname}.${source_tbname}_%s extracte succeed!"%month_time)
				shutil.rmtree(path)
				shutil.rmtree(appendix_path)
			else:
				pri.error("appendix download error!!")
		else:
			pri.error("Type is not exists")

	else:
		print("ScheduleType type is not exists")

	curs_txt.close()


        
if __name__ == '__main__':
	action_datax()
	upload()
