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
sys.path.append('/opt/datatom/dana_appendix_api/script')
from check_datax_log import operate_tables
from send_datax_log import sed_log


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

#文件路径
file_dir='/opt/datatom/dana_appendix_api/data'
jarFile='/opt/datatom/dana_appendix_api/libs/inceptor-driver-5.2.0.jar'
log_path='/opt/datatom/dana_appendix_api/log/'
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
day_time = (datetime.datetime.now() + datetime.timedelta(days = -2)).strftime("%Y%m%d%H%M%S")[0:8]
month_time = (datetime.datetime.now() - relativedelta(months = 1)).strftime("%Y%m%d%H%M%S")[0:6]



#执行datax并把日志写入库
def action_datax():

	ScheduleType = '1'
	if ScheduleType == '1':
		#os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/execute_cfg/huanbaoju_16_88_syrk_t_zp_edz_2.json > /opt/datatom/dana_appendix_api/log/${exec_datax_log}/huanbaoju_16_88_syrk_t_zp_edz_2.log"%addtime)
		os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/execute_cfg/huanbaoju_16_88_syrk_t_zp_edz_2.json > /opt/datatom/dana_appendix_api/log/huanbaoju_16_88_syrk_t_zp_edz_2.log"%addtime)
		#sed_log('huanbaoju_16_88_syrk_t_zp_edz_2')
		operate_tables('/opt/datatom/dana_appendix_api/log/huanbaoju_16_88_syrk_t_zp_edz_2.log', 'gonganju_txt.T_ZP_EDZ_2_%s'%day_time, 'SYRK.T_ZP_EDZ_2','detuo_base.job_run_info')
		pri.ok("table SYRK.T_ZP_EDZ_2 data extraction txt succeed，uploading to inceptor!")
	elif ScheduleType == '3':
		#os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/execute_cfg/huanbaoju_16_88_syrk_t_zp_edz_2.json > /opt/datatom/dana_appendix_api/log/${exec_datax_log}/huanbaoju_16_88_syrk_t_zp_edz_2.log"%addtime)
		os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_appendix_api/execute_cfg/huanbaoju_16_88_syrk_t_zp_edz_2.json > /opt/datatom/dana_appendix_api/log/huanbaoju_16_88_syrk_t_zp_edz_2.log"%addtime)
		#sed_log('huanbaoju_16_88_syrk_t_zp_edz_2')
		operate_tables('/opt/datatom/dana_appendix_api/log/huanbaoju_16_88_syrk_t_zp_edz_2.log', 'gonganju_txt.T_ZP_EDZ_2_%s'%month_time, 'SYRK.T_ZP_EDZ_2','detuo_base.job_run_info')
		pri.ok("table SYRK.T_ZP_EDZ_2 data extraction txt succeed，uploading to inceptor!")
	else:
		print("ScheduleType is not exists")



def upload():

	dirver = 'org.apache.hive.jdbc.HiveDriver'
	conn = jaydebeapi.connect(dirver, 'jdbc:hive2://172.27.148.14:30438/;guardianToken=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH', ['', ''], jarFile)
	curs_load = conn.cursor()
	os.system("curl -i -X PUT \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/?op=MKDIRS&permission=777&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\"")
	path="%s/huanbaoju/SYRK_T_ZP_EDZ_2"%file_dir
	for root, dirs, files in os.walk(path):	
		if not os.path.isdir("%s/SYRK_T_ZP_EDZ_2_split"%path):
			os.system("mkdir -p %s/SYRK_T_ZP_EDZ_2_split"%path)
		for i in range(len(files)):
			os.system("split -l 5000000 %s/%s -d -a 10 %s/SYRK_T_ZP_EDZ_2_split/%s"%(path,files[i],path,files[i]))
		break

	curs_txt = conn.cursor()
	ScheduleType = '1'
	Type = '1'
	if ScheduleType == '1':
		#源库存的是附件本身
		if Type == '1':	
		#新建txt以及orc表
			txt_table = "create table if not exists gonganju_txt.T_ZP_EDZ_2_%s(ID string comment 'ID',ZJHM string comment '证件号码',ZP blob comment '图片',ZPRQ string comment '照片日期',SJGXSJ string comment '数据共享时间',PHOTO_NO string comment '',JLRKSJ string comment '',RID string comment '')ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%day_time
			orc_table = "create table if not exists gonganju_ods.T_ZP_EDZ_2_%s(ID string comment 'ID',ZJHM string comment '证件号码',ZP blob comment '图片',ZPRQ string comment '照片日期',SJGXSJ string comment '数据共享时间',PHOTO_NO string comment '',JLRKSJ string comment '',RID string comment '') stored as hyperdrive;"%day_time
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")
			#上传文件并加载到星环
			for file1,file2,file3 in os.walk("%s/SYRK_T_ZP_EDZ_2_split"%path):
				i=0
				for i in range(len(file3)):
					pri.info("data uploading %s..............."%file3[i])
					os.system("curl -i -X PUT \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\"")
					#-C表示支持断点续传
					#os.system("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					time.sleep(5)
					print("status=",status)
					count = 1
					while (status != 0 and count <= 5):
						print("file %s upload failed,re-uploading!"%file3[i])
						status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
						count = count + 1
					sqlStr = "load data inpath '/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt' into table gonganju_txt.T_ZP_EDZ_2_%s"%day_time
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
				sql_truncate_orc = "truncate table gonganju_ods.T_ZP_EDZ_2"
				curs_truncateorc.execute(sql_truncate_orc)
				pri.ok("truncate orc table gonganju_ods.T_ZP_EDZ_2 succeed")
				curs_truncateorc.close()
			else:
				pri.info("incremental data extraction per day!")
			sql_orc = "insert into gonganju_ods.T_ZP_EDZ_2_%s (ID,ZJHM,ZP,ZPRQ,SJGXSJ,PHOTO_NO,JLRKSJ,RID) select ID,ZJHM,ZP,ZPRQ,SJGXSJ,PHOTO_NO,JLRKSJ,RID  from gonganju_txt.T_ZP_EDZ_2_%s"%(day_time,day_time)
			curs_insertorc.execute(sql_orc)
			pri.ok("insert orc table from txt table succeed!")	
			curs_truncate = conn.cursor()
			sql_truncate = "truncate table gonganju_txt.T_ZP_EDZ_2_%s"%day_time
			curs_truncate.execute(sql_truncate)
			pri.ok("truncate txt table gonganju_txt.T_ZP_EDZ_2_%s succeed!"%day_time)
			curs_load.close()
			curs_insertorc.close()
			curs_truncate.close()
			conn.close()
			pri.ok("table SYRK.T_ZP_EDZ_2_%s extracte succeed!"%day_time)
			os.system("rm -rf %s"%path)
		#源库存的是附件路径
		elif Type == '2':
		#新建txt以及orc表
			txt_table = "create table if not exists gonganju_txt.T_ZP_EDZ_2_%s(ID string comment 'ID',ZJHM string comment '证件号码',ZP blob comment '图片',ZPRQ string comment '照片日期',SJGXSJ string comment '数据共享时间',PHOTO_NO string comment '',JLRKSJ string comment '',RID string comment '')ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%day_time
			orc_table = "create table if not exists gonganju_ods.T_ZP_EDZ_2_%s(ID string comment 'ID',ZJHM string comment '证件号码',ZP blob comment '图片',ZPRQ string comment '照片日期',SJGXSJ string comment '数据共享时间',PHOTO_NO string comment '',JLRKSJ string comment '',RID string comment '') stored as hyperdrive;"%day_time
			appendix_table = ""
			print("xinghuan_txt create table sql:",txt_table)
			print("xinghuan_orc create table sql:",orc_table)
			curs_txt.execute(txt_table)
			curs_txt.execute(orc_table)
			pri.info("---------------------create xinghuan_txt table is success----------------")
			pri.info("---------------------create xinghuan table is success----------------")
			#上传文件并加载到星环
			for file1,file2,file3 in os.walk("%s/SYRK_T_ZP_EDZ_2_split"%path):
				i=0
				for i in range(len(file3)):
					pri.info("data uploading %s..............."%file3[i])
					os.system("curl -i -X PUT \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\"")
					#-C表示支持断点续传
					#os.system("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					time.sleep(5)
					print("status=",status)
					count = 1
					while (status != 0 and count <= 5):
						print("file %s upload failed,re-uploading!"%file3[i])
						status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
						count = count + 1
					sqlStr = "load data inpath '/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt' into table gonganju_txt.T_ZP_EDZ_2_%s"%day_time
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
				sql_truncate_orc = "truncate table gonganju_ods.T_ZP_EDZ_2"
				curs_truncateorc.execute(sql_truncate_orc)
				pri.ok("truncate orc table gonganju_ods.T_ZP_EDZ_2 succeed")
				curs_truncateorc.close()
			else:
				pri.info("incremental data extraction per day!")
			sql_orc = "insert into gonganju_ods.T_ZP_EDZ_2_%s (ID,ZJHM,ZP,ZPRQ,SJGXSJ,PHOTO_NO,JLRKSJ,RID) select ID,ZJHM,ZP,ZPRQ,SJGXSJ,PHOTO_NO,JLRKSJ,RID  from gonganju_txt.T_ZP_EDZ_2_%s"%(day_time,day_time)
			curs_insertorc.execute(sql_orc)
			pri.ok("insert orc table from txt table succeed!")	
			curs_truncate = conn.cursor()
			sql_truncate = "truncate table gonganju_txt.T_ZP_EDZ_2_%s"%day_time
			curs_truncate.execute(sql_truncate)
			pri.ok("truncate txt table gonganju_txt.T_ZP_EDZ_2_%s succeed!"%day_time)
			curs_load.close()
			curs_insertorc.close()
			curs_truncate.close()
			conn.close()
			pri.ok("table SYRK.T_ZP_EDZ_2_%s extracte succeed!"%day_time)
			os.system("rm -rf %s"%path)
		else:
			pri.error("type is not exists")

	elif ScheduleType == '3':
		txt_table = "create table if not exists gonganju_txt.T_ZP_EDZ_2_%s(ID string comment 'ID',ZJHM string comment '证件号码',ZP blob comment '图片',ZPRQ string comment '照片日期',SJGXSJ string comment '数据共享时间',PHOTO_NO string comment '',JLRKSJ string comment '',RID string comment '')ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\u0001';"%month_time
		orc_table = "create table if not exists gonganju_ods.T_ZP_EDZ_2_%s(ID string comment 'ID',ZJHM string comment '证件号码',ZP blob comment '图片',ZPRQ string comment '照片日期',SJGXSJ string comment '数据共享时间',PHOTO_NO string comment '',JLRKSJ string comment '',RID string comment '')clustered by (ID) into 3 buckets stored as orc tblproperties('transactional'='true');"%month_time
		print("xinghuan_txt create table sql:",txt_table)
		print("xinghuan_orc create table sql:",orc_table)
		curs_txt.execute(txt_table)
		curs_txt.execute(orc_table)
		pri.info("---------------------create xinghuan_txt table is success----------------")
		pri.info("---------------------create xinghuan table is success----------------")

		for file1,file2,file3 in os.walk("%s/SYRK_T_ZP_EDZ_2_split"%path):
			i=0
			for i in range(len(file3)):
				pri.info("data uploading %s..............."%file3[i])
				os.system("curl -i -X PUT \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\"")
				#-C表示支持断点续传
				#os.system("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				time.sleep(5)
				print("status=",status)
				count = 1
				while (status != 0 and count <= 5):
					print("file %s upload failed,re-uploading!"%file3[i])
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/SYRK_T_ZP_EDZ_2_split/%s \"http://172.27.148.14:31756/webhdfs/v1/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt?op=CREATE&data=true&guardian_access_token=da30EEF4lIxgm6QQKwpg-M03NIQ5.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					count = count + 1
				sqlStr = "load data inpath '/tmp/detuo/huanbaoju_SYRK_T_ZP_EDZ_2.txt' into table gonganju_txt.T_ZP_EDZ_2_%s"%month_time
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
			sql_truncate_orc = "truncate table gonganju_ods.T_ZP_EDZ_2"
			curs_truncateorc.execute(sql_truncate_orc)
			pri.ok("truncate orc table gonganju_ods.T_ZP_EDZ_2 succeed")
			curs_truncateorc.close()
		else:
			pri.info("incremental data extraction per day!")
		sql_orc = "insert into gonganju_ods.T_ZP_EDZ_2_%s (ID,ZJHM,ZP,ZPRQ,SJGXSJ,PHOTO_NO,JLRKSJ,RID) select ID,ZJHM,ZP,ZPRQ,SJGXSJ,PHOTO_NO,JLRKSJ,RID  from gonganju_txt.T_ZP_EDZ_2_%s"%(month_time,month_time)
		curs_insertorc.execute(sql_orc)
		pri.ok("insert orc table from txt table succeed!")	
		curs_truncate = conn.cursor()
		sql_truncate = "truncate table gonganju_txt.T_ZP_EDZ_2_%s"%month_time
		curs_truncate.execute(sql_truncate)
		pri.ok("truncate txt table gonganju_txt.T_ZP_EDZ_2_%s succeed!"%month_time)
		curs_load.close()
		curs_insertorc.close()
		curs_truncate.close()
		conn.close()
		pri.ok("table SYRK.T_ZP_EDZ_2_%s extracte succeed!"%month_time)
		os.system("rm -rf %s"%path)

	else:
		print("ScheduleType type is not exists")
	curs_txt.close()


        
if __name__ == '__main__':
	action_datax()
	upload()
