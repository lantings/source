#!/usr/bin/python
# -*- coding: UTF-8 -*- 
 
import jaydebeapi
import subprocess
import cx_Oracle
import MySQLdb
import time
import datetime
import json
import os
import math

day_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))[0:8]
jarFile_dameng = '/opt/datatom/dana_api/libs/Dm7JdbcDriver17.jar'

def get_table_count(sourcetype,sourceaddress,sourceip,sourceport,sourcetable,sourceuser,sourcepasswd,xhtable,primary,addtimefield,scheduletype):
	if sourcetype == 'dameng':
		dirver = 'dm.jdbc.driver.DmDriver'
		conn = jaydebeapi.connect(dirver, sourceaddress, [sourceuser, sourcepasswd], jarFile_dameng)
		cursor = conn.cursor()
		print("dameng conn succeed")
		if scheduletype == '1':
			wheredate = "%s >= to_date(%s,'yyyymmdd') - INTERVAL '2' DAY  and %s < to_date(%s,'yyyymmdd') - INTERVAL '1' DAY "%(addtimefield,day_time,addtimefield,day_time)
		elif scheduletype == '2':
			wheredate = "%s >= to_date(%s,'yyyymmdd') - INTERVAL '8' DAY  and %s < to_date(%s,'yyyymmdd') - INTERVAL '1' DAY "%(addtimefield,day_time,addtimefield,day_time)
		elif scheduletype == '3':
			wheredate = "%s >= to_date(to_char((to_date('%s','yyyymmdd') - INTERVAL '1' MONTH),'yyyymm'),'yyyymm')  and %s < to_date(to_char((to_date('%s','yyyymmdd') - INTERVAL '0' MONTH),'yyyymm'),'yyyymm')"%(addtimefield,day_time,addtimefield,day_time)
		else:
			print("scheduletype input error")
		print(wheredate)
		cursor.execute("select count(1) from %s where %s "%(sourcetable,wheredate))
		count = cursor.fetchall()
		return count[0][0]

	elif sourcetype == 'mysql':
		db = sourcetable.split('.')[0]
		table = sourcetable.split('.')[1]
		conn = MySQLdb.connect(sourceip, sourceuser, sourcepasswd, db, int(sourceport),charset='utf8')
		cursor = conn.cursor()
		print("mysql conn succeed")
		if scheduletype == '1':
			wheredate = "%s >= DATE_FORMAT(DATE_SUB(STR_TO_DATE(%s,'%%Y%%m%%d'),INTERVAL 2 DAY),'%%Y%%m%%d') and %s < DATE_FORMAT(DATE_SUB(STR_TO_DATE(%s,'%%Y%%m%%d'),INTERVAL 1 DAY),'%%Y%%m%%d') "%(addtimefield,day_time,addtimefield,day_time)
		elif scheduletype == '2':
			wheredate = "%s >=DATE_FORMAT(DATE_SUB(STR_TO_DATE(%s,'%%Y%%m%%d'),INTERVAL 2 WEEK),'%%Y%%m%%d') and %s < DATE_FORMAT(DATE_SUB(STR_TO_DATE(%s,'%%Y%%m%%d'),INTERVAL 1 WEEK),'%%Y%%m%%d') "%(addtimefield,day_time,addtimefield,day_time)
		elif scheduletype == '3':
			wheredate = "%s >= DATE_FORMAT(DATE_SUB(STR_TO_DATE(%s,'%%Y%%m%%d'),INTERVAL 1 MONTH),'%%Y-%%m') and %s < DATE_FORMAT(STR_TO_DATE(%s,'%%Y%%m%%d'),'%%Y-%%m')"%(addtimefield,day_time,addtimefield,day_time)
		else:
			print("scheduletype input error")
		print(wheredate)
		#starttime = (datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%Y%m%d")
		#endtime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y%m%d") 
		cursor.execute("select count(1) from %s where %s"%(sourcetable,wheredate))
		count = cursor.fetchall()
		return count[0][0]

	elif sourcetype == 'oracle':
		jdbcurl = '%s/%s%s'%(sourceuser,sourcepasswd,sourceaddress.split('thin:')[1])
		conn=cx_Oracle.connect(jdbcurl)
		cursor = conn.cursor()
		print("oracle conn succeed")
		if scheduletype == '1':
			wheredate = "%s >= to_date(%s,'yyyymmdd') - INTERVAL '2' DAY  and %s < to_date(%s,'yyyymmdd') - INTERVAL '1' DAY "%(addtimefield,day_time,addtimefield,day_time)
		elif scheduletype == '2':
			wheredate = "%s >= to_date(%s,'yyyymmdd') - INTERVAL '8' DAY  and %s < to_date(%s,'yyyymmdd') - INTERVAL '1' DAY "%(addtimefield,day_time,addtimefield,day_time)
		elif scheduletype == '3':
			wheredate = "%s >= to_date(to_char((to_date('%s','yyyymmdd') - INTERVAL '1' MONTH),'yyyymm'),'yyyymm')  and %s < to_date(to_char((to_date('%s','yyyymmdd') - INTERVAL '0' MONTH),'yyyymm'),'yyyymm')"%(addtimefield,day_time,addtimefield,day_time)
		else:
			print("scheduletype input error")
		print(wheredate)
		cursor.execute("select count(1) from %s where %s "%(sourcetable,wheredate))
		count = cursor.fetchall()
		return count[0][0]
	else:
		print("sourcetype is not support")
        
        
def get_num(num):
	num = int(num)
	for  i in range(2,num):
		if num % i == 0 :
			return False
		else:
			continue
	if i == num - 1:
		return True

            
def print_num(sourcetype,sourceaddress,sourceip,sourceport,sourcetable,sourceuser,sourcepasswd,xhtable,primary,addtimefield,scheduletype):
	num = get_table_count(sourcetype,sourceaddress,sourceip,sourceport,sourcetable,sourceuser,sourcepasswd,xhtable,primary,addtimefield,scheduletype)
	num = math.ceil(float(num)/1000000)
	if num > 3:
		while True:
			if get_num(num):
				return int(num)
				break
			num += 1
	else:
		num = 3
		return int(num)







if __name__ == '__main__':
	#create_table('dameng','jdbc:dm://10.81.68.20:5236','10.81.68.20','5236','dsjzx.table','SYSDBA','SYSDBA','tdt.test','id','jhpt_update_time')
	#x = get_table_count('mysql','jdbc:mysql://172.26.16.87:3306/test','172.26.16.87','3306','test.test1','root','datatom','tdt.test','id','jhpt_update_time','3')
	#print(x)
	#x = get_table_count('oracle','jdbc:oracle:thin:@172.26.16.88:1522/orcl1','172.26.16.88','1522','syrk.test1','SYRK','SYRK','tdt.test','id','jhpt_update_time','1')
	#print(x)
    y = print_num(x)
    print (y)
    #create_table([{"column_name":"jhpy_update_time","column_type":"varchar(100)","column_desc":"数据生成时间","column_order":1},{"column_name":"jhpy_time","column_type":"varchar(100)","column_desc":"数据时间","column_order":2}],'tdt.test1','tdt.test2','id','1')
