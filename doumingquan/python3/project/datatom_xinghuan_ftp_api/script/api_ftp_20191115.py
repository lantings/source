#coding=utf-8

import tornado.ioloop
import tornado.web
import json
import datetime
import logging
import ConfigParser
from GenerateWorkflowScript_ftp import source_params,etl_cfg_file
from dodox_01907302051 import OperateDodox
#import jwt
from check_params import check_params, check_para_num
#from new_createmsyqljson import CreateJson
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

dodoer = OperateDodox()

#记录工作流情况的表
recordTable = 'detuo_base.task_info'
extimes="-1"
#添加工作流
class add(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")
    def post(self):
        danasip = "172.27.148.53"
        res = self.request.body.decode('utf-8')
        res = json.loads(res)

        #判断参数
        keysList=["UnitId","UnitName","Ftppath","SourceTableName","XinghuanAddress","HttpfsAddress","XinghuanTableName","MappingList","XinghuanOrcTableName","TargetList","Field","WorkflowTime","Execrate","PrimaryKey"]
        lostColumns,ress = check_para_num(res,keysList)
        if len(lostColumns) > 0:
           self.write(ress)
        else:
            UnitId = res['UnitId']
            UnitName = res['UnitName']

            NotionalPoolingType = res['NotionalPoolingType']
	    unitname,ftpip,ftpport,ftpusername,ftppasswd = source_params(UnitId,Notionalpoolingtype)
            XinghuanAddress = res['XinghuanAddress']
            HttpfsAddress = res['HttpfsAddress']
            SourceTableName = res['SourceTableName']
            XinghuanTableName = res['XinghuanTableName']
            XinghuanOrcTableName = res['XinghuanOrcTableName']
            
            MappingList = res['MappingList']
            TargetList = res['TargetList']
            Field = res['Field']
            PrimaryKey = res["PrimaryKey"]
            #定时策略
            WorkflowTime = res['WorkflowTime']
            ScheduleType = WorkflowTime['ScheduleType']
            ScheduleDetail = WorkflowTime['ScheduleDetail']
            Execrate = res['Execrate']
            
 	    print(ftpip)
            ipSplit = ftpip.split('.')
            tableName = SourceTableName
            #source_tbname = SourceTableName.split('.')[1]
            #source_dbname = SourceTableName.split('.')[0]
            WorkflowName = "{un}_ftp_{ipa}_{ipb}_{tb}".format(un=unitname.lower(), ipa= str(ipSplit[2]), ipb=str(ipSplit[3]), tb=tableName.lower())
            #WorkflowName = "{un}_{tb}".format(un=unitname.lower(),tb=tableName.lower())
            confName = WorkflowName+'.conf'
            
            file_name = XinghuanTableName.split(".")[1]     #表名
            db_name = XinghuanTableName.split(".")[0]       #数据库名

           
            with open('/opt/datatom/dana_ftp_api/table_cfg/{cfg}'.format(cfg = confName),'w') as cfgmaker:
                cfg_str = "[info]\n"
                cfg_str += "UnitId="+res['UnitId'].strip()+"\n"
                cfg_str += "UnitName="+res['UnitName'].strip()+"\n"
                cfg_str += "XinghuanAddress="+res['XinghuanAddress'].encode('utf-8').strip()+"\n"
                cfg_str += "HttpfsAddress="+res['HttpfsAddress'].encode('utf-8').strip()+"\n"
               	cfg_str += "Notionalpoolingtype="+res['Notionalpoolingtype'].strip()+"\n"
                cfg_str += "Ftppath="+res['Ftppath'].encode('utf-8').strip()+"\n"
                cfg_str += "SourceTableName="+res['SourceTableName'].strip()+"\n"
                cfg_str += "PrimaryKey="+res['PrimaryKey'].strip()+"\n"
                cfg_str += "XinghuanTableName="+res['XinghuanTableName'].strip()+"\n"
                cfg_str += "XinghuanOrcTableName="+res['XinghuanOrcTableName'].strip()+"\n" 
                cfg_str += "MappingList="+','.join(res['MappingList']).strip()+"\n"
                cfg_str += "TargetList="+','.join(res['TargetList']).strip()+"\n"
                cfg_str += "Field="+str(res['Field']).encode('utf-8')+"\n"
                cfg_str += "ScheduleType="+str(WorkflowTime['ScheduleType'])+"\n"
                cfg_str += "ScheduleDetail="+WorkflowTime['ScheduleDetail']+"\n"
                cfg_str += "Execrate="+str(res['Execrate'])+"\n"
                cfgmaker.write(cfg_str.encode('utf-8')) 
	    print("conf file is created")

	    etl_cfg_file(UnitId,WorkflowName,NotionalPoolingType)
	    res = dodoer.create_all_nodes(unitname,['/opt/datatom/dana_ftp_api/execute_cfg/%s.py'%(WorkflowName)], WorkflowName,UnitName,'.py','python',danasip,-1,ScheduleDetail,ScheduleType,recordTable,'datatom')	
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
            
#下线任务
class ofline(tornado.web.RequestHandler):
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
            res = dodoer.stop_workflow(id,recordTable)
            self.write(json.loads(res.encode('utf-8'))) 
            
#上线接口
class start(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")
    def post(self):
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
           
application = tornado.web.Application([
    (r"/dana/workflow/add", add),
    (r"/dana/workflow/delete", delete),
    (r"/dana/workflow/start", runnew),
    (r"/dana/workflow/stop", stopjob),
    (r"/dana/workflow/ofline", ofline),
    (r"/dana/workflow/startwork", start)
])
if __name__ == "__main__":
    application.listen(12308)
    tornado.ioloop.IOLoop.instance().start()
