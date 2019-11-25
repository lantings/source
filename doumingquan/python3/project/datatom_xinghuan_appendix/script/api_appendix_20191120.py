#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tornado.ioloop
import tornado.web
import json
import datetime
import logging
import ConfigParser
import os
import sys
from GenerateWorkflowScript_appendix import source_params,datax_update,etl_update,datax_cfg_file,datax_all_file,etl_all_file,etl_cfg_file
from dodox_01907302051 import OperateDodox
#import jwt
from check_params import check_params, check_para_num
#from new_createmsyqljson import CreateJson
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
#from ase import pkcs7padding,pkcs7unpadding,encrypt,decrypt,get_key
from db import OperDb
dodoer = OperateDodox()

#记录工作流情况的表
recordTable = 'detuo_base.task_info'
#添加工作流
class add(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")
    def post(self):
        danasip = "172.27.148.53"
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        print(res)

        #判断参数
        keysList=['UnitId','UnitName','XinghuanAddress','Ftppath','HttpfsAddress','SourceTableName','XinghuanTableName','XinghuanOrcTableName','PrimaryKey','MappingList','Exectimes','WorkflowTime','AddTimefield','TargetList','ColumnType','Execrate','Field','Type','AppendixFiled','OrcTableDesc','NotionalPoolingType','ExecUser']
        lostColumns,ress = check_para_num(res,keysList)
        print(lostColumns)
        print(ress)
        if len(lostColumns) > 0:
           self.write(ress)
        else:
            print("2222222222222222222222222222")
            UnitId = res['UnitId']
            UnitName = res['UnitName']
            XinghuanAddress = res['XinghuanAddress']
            Ftppath=res['Ftppath']
            HttpfsAddress = res['HttpfsAddress']
            XinghuanTableName = res['XinghuanTableName']
            XinghuanOrcTableName = res['XinghuanOrcTableName']
            MappingList = res['MappingList']
            TargetList = res['TargetList']
            SourceTableName = res['SourceTableName']
            Dbname = unicode.encode(SourceTableName.split('.')[0])
            PrimaryKey = res['PrimaryKey'] 
            Exectimes = res['Exectimes']
            #获取定时策略
            WorkflowTime = res['WorkflowTime']
            ScheduleType = WorkflowTime['ScheduleType']
            ScheduleDetail = WorkflowTime['ScheduleDetail']
            AddTimefield = res['AddTimefield']
            ColumnType = res['ColumnType']
            Execrate = res['Execrate']
            Field = res['Field']
            Type=res['Type']
            ExecUser=res['ExecUser']
            AppendixFiled=res['AppendixFiled']
            OrcTableDesc=res['OrcTableDesc']
            NotionalPoolingType=res['NotionalPoolingType']

            unitname,databasetype,sourceip,sourceport,sourcedbname,sourceaddress,sourceusername,sourcepassword,ftpip,ftpport,ftpusername,ftppasswd = source_params(UnitId,Dbname,NotionalPoolingType)
            print("1111111111111111111111111",UnitId)
            ipSplit = sourceip.split('.')
            tableName = SourceTableName.replace('.','_')

            WorkflowName = "{un}_{notional}_{ipa}_{ipb}_{tb}".format(un=unitname.lower(), notional=NotionalPoolingType,ipa= str(ipSplit[2]), ipb=str(ipSplit[3]), tb=tableName.lower())
            confName = WorkflowName+'.conf'

            with open('/opt/datatom/dana_appendix_api/table_cfg/{cfg}'.format(cfg = confName),'w') as cfgmaker:
                cfg_str = "[info]\n"
                cfg_str += "UnitId="+res['UnitId'].strip()+"\n"
                cfg_str += "UnitName="+res['UnitName'].strip()+"\n"
                cfg_str += "XinghuanAddress="+res['XinghuanAddress'].encode('utf-8').strip()+"\n"
                cfg_str += "Ftppath="+res['Ftppath'].strip()+"\n"
                cfg_str += "HttpfsAddress="+res['HttpfsAddress'].encode('utf-8').strip()+"\n"
                cfg_str += "XinghuanTableName="+res['XinghuanTableName'].strip()+"\n"
                cfg_str += "XinghuanOrcTableName="+res['XinghuanOrcTableName'].strip()+"\n"                
                cfg_str += "MappingList="+','.join(res['MappingList']).strip()+"\n"
                cfg_str += "TargetList="+','.join(res['TargetList']).strip()+"\n"
                cfg_str += "SourceTableName="+res['SourceTableName'].strip()+"\n"
                cfg_str += "PrimaryKey="+res['PrimaryKey'].strip()+"\n"
                cfg_str += "Exectimes="+str(res['Exectimes'])+"\n"
                cfg_str += "ScheduleType="+str(WorkflowTime['ScheduleType'])+"\n"
                cfg_str += "ScheduleDetail="+WorkflowTime['ScheduleDetail']+"\n"
                cfg_str += "AddTimefield="+res['AddTimefield'].strip()+"\n"
                cfg_str += "ColumnType="+res['ColumnType'].strip()+"\n"
                cfg_str += "Execrate="+str(res['Execrate'])+"\n"
                cfg_str += "Field="+str(res['Field']).encode('utf-8')+"\n"
                cfg_str += "AppendixFiled="+res['AppendixFiled'].strip()+"\n"
                cfg_str += "OrcTableDesc="+res['OrcTableDesc'].strip()+"\n"
                cfg_str += "NotionalPoolingType="+res['NotionalPoolingType'].strip()+"\n"
                cfg_str += "ExecUser="+res['ExecUser'].strip()+"\n"
                cfg_str += "Type="+str(res['Type'])+"\n"

                cfgmaker.write(cfg_str.encode('utf-8'))
            print("conf file is created")

            #生成datax配置和调用脚本
        datax_update(UnitId,WorkflowName,Dbname)
        datax_cfg_file(UnitId,WorkflowName,Dbname)
        datax_all_file(UnitId,WorkflowName,Dbname)
        etl_update(UnitId,WorkflowName,Dbname)
        etl_all_file(UnitId,WorkflowName,Dbname)
        etl_cfg_file(UnitId,WorkflowName,Dbname)
        res = dodoer.create_all_nodes(unitname,['/opt/datatom/dana_appendix_api/execute_cfg/%s.py'%(WorkflowName)], WorkflowName,UnitName,'.py','python',danasip,Exectimes,ScheduleDetail,ScheduleType,recordTable,ExecUser)
        self.write(json.loads(res))


#下线任务
class ofline(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #检查参数
        keysList=['Workflowid']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:     
            id = res['Workflowid'].strip()
            res = dodoer.stop_workflow(id,recordTable)
            print(res)
            self.write(res)  

#下线任务并删除工作流
class delete(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #检查参数
        keysList=['Workflowid']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:     
            id = res['Workflowid'].strip()
            res = dodoer.del_undown_workflow(id,recordTable)
            self.write(json.loads(res.encode('utf-8')))

#手动运行工作流
class runnew(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)

        #判断参数
        keysList=["userid","Workflowid"]
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:
            userid = res['userid']
            wfid = res['Workflowid']
            res = dodoer.wait_runnew(wfid, userid)
            logger.info(res)
            self.write(json.loads(res))
#手动停止任务运行
class stopjob(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()   
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        print(res)
        #判断参数
        keysList=["Workflowid"]
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:
            wfid = res['Workflowid']
            res = dodoer.stop_job(wfid)
            logger.info(res)
            self.write(json.loads(res))

#上线接口
class start(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #判断参数
        keysList=['Workid','Nodeip','Exectimes','WorkflowTime','WorkflowName']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:
            wid = res['Workid']
            node = res['Nodeip']
            extimes = res['Exectimes']
            #获取定时策略
            workflowTime = res['WorkflowTime']
            scheduleType = workflowTime['ScheduleType']
            scheduleDetail = workflowTime['ScheduleDetail']
            workflowName = res['WorkflowName']
            #scripid = res['Scripid']

            res = dodoer.start_workflow(wid,extimes,scheduleDetail,scheduleType,node,workflowName,recordTable)
            self.write(json.loads(res))

#登录接口
class login(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #a
        user = res['user']
        passwords =res['passwd']
        data = dodoer.login_ds(user,passwords)
        if data:
            res = {"code":200,"result":data}
            #res = json.dumps(res)
        else:
            res = {"code":1003,"result":"请重新登录"}
            #res = json.dumps(res)
        self.write(json.loads(res))
 
class getjob(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #检查参数
        keysList=['userid']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:     
            id = res['userid'].strip()
            res = dodoer.list_job(id)
            print(res)
            self.write(res)  
         
class get_last_job_status(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #检查参数
        keysList=['wfid','userid']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:     
            wfid = res['wfid']
            userid = res['userid']
            res = dodoer.get_last_job_status(wfid,userid)
            print(res)
            self.write(res) 
           
class fail_runnew(tornado.web.RequestHandler):
    def post(self):
        dodoer = OperateDodox()
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        #检查参数
        keysList=['wfid','userid']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:     
            wfid = res['wfid']
            userid = res['userid']
            res = dodoer.fail_runnew(wfid,userid)
            print(res)
            self.write(res)

application = tornado.web.Application([
    (r"/dana/workflow/add", add),
    (r"/dana/workflow/delete", delete),
    (r"/dana/workflow/start", runnew),
    (r"/dana/workflow/stop", stopjob),
    (r"/dana/workflow/ofline", ofline),
    (r"/dana/workflow/startwork", start),
    (r"/dana/workflow/login", login),
    (r"/dana/workflow/getjob", getjob),
    (r"/dana/workflow/get_last_job_status", get_last_job_status),
    (r"/dana/workflow/fail_runnew", fail_runnew)
])
if __name__ == "__main__":
    application.listen(12310)
    tornado.ioloop.IOLoop.instance().start()
