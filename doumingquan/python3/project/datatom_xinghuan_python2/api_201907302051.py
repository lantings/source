#coding=utf-8

import tornado.ioloop
import tornado.web
import json
import datetime
import logging
import ConfigParser
from GenerateWorkflowScript import source_params,datax_update,etl_update,datax_cfg_file,datax_all_file,etl_all_file,etl_cfg_file
from dodox_01907302051 import OperateDodox
#import jwt
from check_params import check_params, check_para_num
#from new_createmsyqljson import CreateJson
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

dodoer = OperateDodox()

#记录工作流情况的表
recordTable = 'public.task_info'
#添加工作流
class add(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")
    def post(self):
        res = self.request.body.decode('utf-8')
        res = json.loads(res)

        #判断参数
        keysList=['UnitId','UnitName','XinghuanAddress','HttpfsAddress','SourceTableName','XinghuanTableName','MappingList','Exectimes','WorkflowTime','AddTimefield','TargetList','Execrate']
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:
            UnitId = res['UnitId']
            UnitName = res['UnitName']
            XinghuanAddress = res['XinghuanAddress']
            HttpfsAddress = res['HttpfsAddress']
            SourceTableName = res['SourceTableName']
            Dbname = unicode.encode(SourceTableName.split('.')[0])
            PrimaryKey = res['PrimaryKey'] 
            XinghuanTableName = res['XinghuanTableName']
            XinghuanOrcTableName = res['XinghuanOrcTableName']
            MappingList = res['MappingList']
            Exectimes = res['Exectimes']
            #获取定时策略
            WorkflowTime = res['WorkflowTime']
            ScheduleType = WorkflowTime['ScheduleType']
            ScheduleDetail = WorkflowTime['ScheduleDetail']
            TargetList = res['TargetList']
            AddTimefield = res['AddTimefield']
            ColumnType = res['ColumnType']
            Execrate = res['Execrate']
            unitname,databasetype,sourceip,sourceport,sourcedbname,sourceaddress,sourceusername,sourcepassword = source_params(UnitId, Dbname)
            #make conf name
            #unitname = 'qingxiangju'
            #sourceip = '172.10.8.103'
            #SourceTableName = 'db.test'
            ipSplit = sourceip.split('.')
            tableName = SourceTableName.replace('.','_')

            WorkflowName = "{un}_{ipa}_{ipb}_{tb}".format(un=unitname.lower(), ipa= str(ipSplit[2]), ipb=str(ipSplit[3]), tb=tableName.lower())
            confName = WorkflowName+'.conf'
            with open('/opt/datatom/dana_api/table_cfg/{cfg}'.format(cfg = confName),'w') as cfgmaker:
                cfg_str = "[info]\n"
                cfg_str += "UnitId="+res['UnitId'].strip()+"\n"
                cfg_str += "UnitName="+res['UnitName'].strip()+"\n"
                cfg_str += "XinghuanAddress="+res['XinghuanAddress'].encode('utf-8').strip()+"\n"
                cfg_str += "HttpfsAddress="+res['HttpfsAddress'].encode('utf-8').strip()+"\n"
                cfg_str += "SourceTableName="+res['SourceTableName'].strip()+"\n"
                cfg_str += "PrimaryKey="+res['PrimaryKey'].strip()+"\n"
                cfg_str += "XinghuanTableName="+res['XinghuanTableName'].strip()+"\n"
                cfg_str += "XinghuanOrcTableName="+res['XinghuanOrcTableName'].strip()+"\n"                
                cfg_str += "MappingList="+','.join(res['MappingList']).strip()+"\n"
                #cfg_str += "MappingList="+str(','.join(res['MappingList']).encode('utf-8').strip().split(','))+"\n"
                cfg_str += "Exectimes="+str(res['Exectimes'])+"\n"
                cfg_str += "ScheduleType="+str(WorkflowTime['ScheduleType'])+"\n"
                cfg_str += "ScheduleDetail="+WorkflowTime['ScheduleDetail']+"\n"
                cfg_str += "AddTimefield="+res['AddTimefield'].strip()+"\n"
                cfg_str += "ColumnType="+res['ColumnType'].strip()+"\n"
                cfg_str += "TargetList="+','.join(res['TargetList']).strip()+"\n"
                cfg_str += "Execrate="+str(res['Execrate'])
                cfgmaker.write(cfg_str.encode('utf-8'))
            #检查传入的参数格式
            #re_info = check_params(UnitId, UnitName, XinghuanAddress, HttpfsAddress, SourceTableName, PrimaryKey,XinghuanTableName, XinghuanOrcTableName, MappingList, Exectimes, WorkflowTime,AddTimefield,  ColumnType)
            #if re_info == 1:
                #创建相关配置
            #    res = jsonMaker.touch_para(username, passwd, column, table, ip, port, sid, columnType, timecolumn)
            #    self.write(res)
            #else:
            #    self.write(re_info)

            #生成datax配置和调用脚本
            datax_update(UnitId,WorkflowName,Dbname)
            datax_cfg_file(UnitId,WorkflowName,Dbname)
            datax_all_file(UnitId,WorkflowName,Dbname)
            etl_update(UnitId,WorkflowName,Dbname)
            etl_all_file(UnitId,WorkflowName,Dbname)
            etl_cfg_file(UnitId,WorkflowName,Dbname)

            #检查传入的参数格式
            #re_info = check_params(UnitId, UnitName, XinghuanAddress, HttpfsAddress, XinghuanTableName, Exectimes, AddTimefield,  columnType, timecolumn, operation_flag)
            #if re_info == 1:
                #创建相关配置
            #    res = jsonMaker.touch_para(username, passwd, column, table, ip, port, sid, columnType, timecolumn)
            #    self.write(res)
            #else:
            #    self.write(re_info)
            res = dodoer.create_all_nodes(unitname,['/opt/datatom/dana_api/execute_cfg/%s.py'%(WorkflowName)], WorkflowName,UnitName,'.py','python','172.26.16.90',Exectimes,ScheduleDetail,ScheduleType,recordTable)
            self.write(json.loads(res))

#下线任务并删除工作流
class delete(tornado.web.RequestHandler):
    def post(self):
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
        res = self.request.body.decode('utf-8')
        res = json.loads(res)

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

application = tornado.web.Application([
    (r"/dana/workflow/add", add),
    (r"/dana/workflow/delete", delete),
    (r"/dana/workflow/start", runnew),
    (r"/dana/workflow/stop", stopjob)
])
if __name__ == "__main__":
    application.listen(12306)
    tornado.ioloop.IOLoop.instance().start()
