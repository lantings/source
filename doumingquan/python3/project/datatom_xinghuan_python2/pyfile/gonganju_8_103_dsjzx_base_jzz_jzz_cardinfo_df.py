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
		#os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_api/execute_all/gonganju_8_103_dsjzx_base_jzz_jzz_cardinfo_df.json > /opt/datatom/dana_api/log/${exec_datax_log}/gonganju_8_103_dsjzx_base_jzz_jzz_cardinfo_df.log"%addtime)
		os.system("python /opt/datatom/datax/bin/datax.py -p \"-Dtimecolumn=%s\" /opt/datatom/dana_api/execute_all/gonganju_8_103_dsjzx_base_jzz_jzz_cardinfo_df.json > /opt/datatom/dana_api/log/gonganju_8_103_dsjzx_base_jzz_jzz_cardinfo_df.log"%addtime)
		operate_tables('/opt/datatom/dana_api/log/gonganju_8_103_dsjzx_base_jzz_jzz_cardinfo_df.log', 'gonganju_txt_ods.base_jzz_jzz_cardinfo_df', 'dsjzx.base_jzz_jzz_cardinfo_df','public.job_run_info')
		pri.ok("table dsjzx.base_jzz_jzz_cardinfo_df data extraction txt succeed，uploading to inceptor!")
	except Exception as e:
		s = sys.exc_info()


def upload():
	try:
		dirver = 'org.apache.hive.jdbc.HiveDriver'
		conn = jaydebeapi.connect(dirver, 'jdbc:hive2://172.17.148.189:30925/gonganju_txt_ods;guardianToken=YRzeh1lLQQETtBMYg5Sd-851RZ52.TDH', ['', ''], jarFile)
		curs = conn.cursor()
		os.system("curl -i -X PUT \"http://172.17.148.189:32228/webhdfs/v1/tmp/detuo/?op=MKDIRS&permission=777&guardian_access_token=YRzeh1lLQQETtBMYg5Sd-851RZ52.TDH\"")
		path="%s/gonganju/dsjzx_base_jzz_jzz_cardinfo_df"%file_dir
		for root, dirs, files in os.walk(path):	
			if not os.path.isdir("%s/dsjzx_base_jzz_jzz_cardinfo_df_split"%path):
				os.system("mkdir -p %s/dsjzx_base_jzz_jzz_cardinfo_df_split"%path)
			for i in range(len(files)):
				os.system("split -l 5000000 %s/%s -d -a 10 %s/dsjzx_base_jzz_jzz_cardinfo_df_split/%s"%(path,files[i],path,files[i]))
			break
		#上传文件并加载到星环
		for file1,file2,file3 in os.walk("%s/dsjzx_base_jzz_jzz_cardinfo_df_split"%path):
			i=0
			for i in range(len(file3)):
				os.system("curl -i -X PUT \"http://172.17.148.189:32228/webhdfs/v1/tmp/detuo/gonganju_dsjzx_base_jzz_jzz_cardinfo_df.txt?op=CREATE&guardian_access_token=YRzeh1lLQQETtBMYg5Sd-851RZ52.TDH\"")
				#-C表示支持断点续传
				#os.system("curl -i -C - -X PUT -T %s/dsjzx_base_jzz_jzz_cardinfo_df_split/%s \"http://172.17.148.189:32228/webhdfs/v1/tmp/detuo/gonganju_dsjzx_base_jzz_jzz_cardinfo_df.txt?op=CREATE&data=true&guardian_access_token=YRzeh1lLQQETtBMYg5Sd-851RZ52.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				pri.info("data uploading...............")
				status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/dsjzx_base_jzz_jzz_cardinfo_df_split/%s \"http://172.17.148.189:32228/webhdfs/v1/tmp/detuo/gonganju_dsjzx_base_jzz_jzz_cardinfo_df.txt?op=CREATE&data=true&guardian_access_token=YRzeh1lLQQETtBMYg5Sd-851RZ52.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
				time.sleep(5)
				print("status=",status)
				count = 1
				while (status != 0 and count <= 5):
					print("file %s upload failed,re-uploading!"%file3[i])
					status,out=commands.getstatusoutput("curl -i -C - -X PUT -T %s/dsjzx_base_jzz_jzz_cardinfo_df_split/%s \"http://172.17.148.189:32228/webhdfs/v1/tmp/detuo/gonganju_dsjzx_base_jzz_jzz_cardinfo_df.txt?op=CREATE&data=true&guardian_access_token=YRzeh1lLQQETtBMYg5Sd-851RZ52.TDH\" -H \"Content-Type:application/octet-stream\""%(path,file3[i]))
					count = count + 1
				sqlStr = "load data inpath '/tmp/detuo/gonganju_dsjzx_base_jzz_jzz_cardinfo_df.txt' into table gonganju_txt_ods.base_jzz_jzz_cardinfo_df"
				curs.execute(sqlStr)
			break
		pri.ok("data upload to hdfs succeed")
		curs2 = conn.cursor()	
		#加载数据到事务表
		Execrate = '1'
		Execrate = str(Execrate)
		if Execrate == '2':
			pri.info("Full data extraction per day!")
			curs4 = conn.cursor()
			sql_truncate_orc = "truncate table gonganju_orc_ods.base_jzz_jzz_cardinfo_df"
			curs4.execute(sql_truncate_orc)
			pri.ok("truncate orc table gonganju_orc_ods.base_jzz_jzz_cardinfo_df succeed")
			curs4.close()
		else:
			pri.info("incremental data extraction per day!")
		sql_orc = "insert into gonganju_orc_ods.base_jzz_jzz_cardinfo_df (apptype,apptype_hz,regcode,chidcard,chname,sortcode,certinum,enrolid,cardid,atr,version,facedate,facedate_dt,validdate,validdate_dt,recokdate,reusenum,cardstatus,cardstatus_hz,cardstadate,statusunitcode,statusunitcode_hz,oprlattice,oprlattice_hz,confirmstatus,confirmdate,confirmdate_dt,latgetcard,latgetcard_hz,latgetdate,pergetdate,errorreason,timestamp,createtime,createtime_dt,reserved,updtuser,updttime,updttime_dt,policeid,policeid_hz,dwd_loadtime,dwd_updatetime,dwd_yxbz,dt,jhpt_update_time,jhpt_delete) select apptype,apptype_hz,regcode,chidcard,chname,sortcode,certinum,enrolid,cardid,atr,version,facedate,facedate_dt,validdate,validdate_dt,recokdate,reusenum,cardstatus,cardstatus_hz,cardstadate,statusunitcode,statusunitcode_hz,oprlattice,oprlattice_hz,confirmstatus,confirmdate,confirmdate_dt,latgetcard,latgetcard_hz,latgetdate,pergetdate,errorreason,timestamp,createtime,createtime_dt,reserved,updtuser,updttime,updttime_dt,policeid,policeid_hz,dwd_loadtime,dwd_updatetime,dwd_yxbz,dt,jhpt_update_time,jhpt_delete  from gonganju_txt_ods.base_jzz_jzz_cardinfo_df"
		curs2.execute(sql_orc)
		pri.ok("insert orc table from txt table succeed!")	
		curs3 = conn.cursor()
		sql_truncate = "truncate table gonganju_txt_ods.base_jzz_jzz_cardinfo_df"
		curs3.execute(sql_truncate)
		pri.ok("truncate txt table gonganju_txt_ods.base_jzz_jzz_cardinfo_df succeed!")
		curs.close()
		curs2.close()
		curs3.close()
		conn.close()
		pri.ok("table dsjzx.base_jzz_jzz_cardinfo_df extracte succeed!")
	except Exception as e:
		s = sys.exc_info()
		

        
if __name__ == '__main__':
	action_datax()
	upload()
