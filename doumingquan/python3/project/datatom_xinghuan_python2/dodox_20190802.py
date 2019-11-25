#coding=utf-8

"""
创建文件夹
#@dirName, 文件夹名称
#@moduleFlag 类型（已经写死了）
上传脚本文件
#@partion, 与dirName相同
#@filePath 需要上传的脚本的绝对路径
新建工作流
#partion,与dirName相同
#taskName,脚本名称
#des，每张表的来源系统_中文名称
查找相应的脚本和工作流id
@keyValue, keyValue脚本去掉后缀的名称
@moduleFlag, 类型（已经写死了）
@postfix， 后缀名
#保存工作流
#@res_wk, 脚本中获取，不用传递
#@res_de, 脚本中获取，不用传递
#@'python', 脚本类型
设置任务调度
#node, 任务运行节点
#extimes, 任务运行次数
#wfId, 任务流id
#scheduleDetail, 调度细节
#scheduleType 调度类型
(dirName,filePathList,taskName,des,postfix,scriptType,node,extimes,scheduleDetail,scheduleType)
"""

import requests
import json
import hashlib
import logging
import sys
from db import OperDb
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OperateDodox():
    def __init__(self):
        self.dber = OperDb()
        self.login_url ="http://172.26.16.90/danastudio/login"
        self.create_url= "http://127.0.0.1/danastudio/ants/folder/create"
        self.upload_url = "http://172.26.16.90/danastudio/dodox/filemanager/file/upload"
        self.workflow_url = "http://172.26.16.90/danastudio/ants/workflow/new"
        self.script2wf_url = "http://172.26.16.90/danastudio/ants/workflow/save"
        self.listall_url = "http://172.26.16.90/danastudio/ants/folder/list"
        #self.search_url = "http://172.26.16.90/danastudio/ants/develop/search"
        self.submit_url = "http://172.26.16.90/danastudio/ants/workflow/submit"
        self.select_script_url = "http://172.26.16.90/danastudio/ants/"
        self.list_job_url = "http://172.26.16.90/danastudio/dodox/job/list"
        self.runnow_url = "http://172.26.16.90/danastudio/dodox/job/runnow"
        self.get_log_url = "http://172.26.16.90/danastudio/dodox/job/record/get"
        self.new_dev_url = "http://172.26.16.90/danastudio/ants/develop/new/dev"
        self.down_url = "http://172.26.16.90/danastudio/ants/workflow/down"
        self.del_wf_url = "http://172.26.16.90/danastudio/ants/workflow/delete"
        self.stop_url = "http://172.26.16.90/danastudio/dodox/job/stop"
        self.refresh_token_url = "http://172.26.16.90/danastudio/refresh_token"

        self.token = self.refresh_token()
        if self.token.find('Bearer') == -1:
            logger.info('token is error, please check public.token_info and dana')
            return self.token()

    #md5加密
    def md5(self,para):
        m2 = hashlib.md5()
        m2.update(para)
        return m2.hexdigest()

    #创建文件夹
    def create_dir(self,dirName,moduleFlag):
        url= "http://127.0.0.1/danastudio/ants/folder/create"
        data ={
            "dirname":dirName,
            "module":moduleFlag
        }
        res = self.request_func(data,self.create_url)
        return res
    def login_ds(self,user,psword):
        data = {
            "username": user,
            "password": self.md5(psword)
        }
        data = json.dumps(data)
        res = requests.post(self.login_url, data).json()
        if res['code'] == 200:
            token = res['result']['token']
            logger.info(token)
        else:
            pass



    def refresh_token(self):
        token_sql = "select token from public.token_info"
        res_token = self.dber.select_sql(token_sql)
        if len(res_token) == 1:
            token = res_token[0][0]
        else:
            res = {"code":10003,"result":"token记录表不存在，请联系厂家"}
            res = json.dumps(res)
            return res
        headers = {
            "Authorization": token
        }
        response = requests.post(self.refresh_token_url, headers = headers)
        res = response.text
        if res.find('expire') != -1:
            token = "Bearer %s"%(json.loads(res)['token'])
            print(token)
            dataDict = {"token": token}
            whereDict = {"1" : "1"}
            self.dber.update_sql('public.token_info',dataDict, whereDict)
            return token
        else:
            return res
        


    #上传脚本文件
    def upload_script(self, dirName, filePath):
        files = {'file':open(filePath,'rb')}
        payload={
            'filepath':'/var/dana/dodox/filemanager/file/admin/'+dirName,
            'force':True
            }

        headers = {
            "Authorization": self.token
        }
        response = requests.post(self.upload_url, data=payload, files = files, headers=headers)
        res = response.text
        return res

    #新建开发脚本
    def new_dev(self, scriptName, context, dirname, scriptType):
        data = {
            "dirname": dirname,
            "isforce": True,
            "name": scriptName,
            "notetype": scriptType,
            "content":context
        }
        res = self.request_func(data,self.new_dev_url)
        return res

    #创建新的工作流
    def new_workflow(self, dirName, taskName, des):
        data = {
            "name": taskName,
            "description": des,
            "tags":[],
            "dirname": dirName
            }
        res = self.request_func(data,self.workflow_url)
        return res

    #获取所有的脚本文件夹
    def get_allDirId(self):
        data = {
            "listall": true,
            "module": "develop"
        }
        res = self.request_func(data,self.listall_url)
        return res

    #根据脚本文件夹名称获取脚本名称
    def get_allScript_id(self,dirId):
        data = {
            "dirid": "AWv4oL80BZ1xJXgBM0sb",
            "listall": true,
            "page": 1,
            "perpage": 10000
        }
        res = self.request_func(data,self.search_url)
        return res

    #查询文件
    def select_dir(self, taskName, moduleFlag, postfix):
        data = {
            "listall": False, 
            "page": 1, 
            "perpage": 10000
        }
        if moduleFlag == 'develop':
            data['selectDir'] = ""
        else:
            data['dirid'] = ""
            data['sorttype'] = 0
        headers = {
            "Authorization": self.token
        }       
        data = json.dumps(data)
        select_script_url = self.select_script_url+moduleFlag+"/search"
        print(select_script_url)
        response = requests.post(select_script_url,headers = headers, data = data)
        res = response.json()
        if res['code'] == 200:
            if moduleFlag == 'develop':
                if len(res['result']['list']) > 0:
                    for i in res['result']['list']:
                        if i['notename'] == taskName+postfix:
                            sid = i['id']
            else:
                if len(res['result']) > 0:
                    for i in res['result']:
                        if i['name'] == taskName:
                            sid = i['id']
        else:
            sid = 0

        return sid,res
    #保存工作流
    def add_script_to_workflow(self, wfId, scriptId, scriptType, taskName):
        data = {
            "id": wfId,
            "subjob": [{
                "subid": 1,
                "cid": scriptId,
                "ctype": scriptType,
                "name": taskName,    
                "x": 158,
                "y": 119
            }]
        }
        res = self.request_func(data,self.script2wf_url)
        return res
    
    #设置任务调度
    def submit_workflow(self, node, extimes, wfId, scheduleDetail, scheduleType):
        data = {
            "assignnode": node,
            "exectimes": extimes,
            "id": wfId,
            "scheduledetail": scheduleDetail,
            "scheduletype": scheduleType
            }
        res = self.request_func(data,self.submit_url)
        return res
    
    #创建整个工作流
    def create_all_nodes(self, dirName,filePathList,taskName,des,postfix,scriptType,node,extimes,scheduleDetail,scheduleType,recordTable):
        #在新建任务的时候检验工作流是否已经创建过，并上线
        ssql = "select * from {recordTable} where workflowname = '{taskName}'".format(recordTable = recordTable,taskName=taskName)
        resData = self.dber.select_sql(ssql)
        if len(resData) == 1:
            wfid = resData[0][1]
            status = resData[0][4]
            if status == 'up':
                #del_info = self.del_undown_workflow(wfid,recordTable)
                res = {"code":10003,"result":"此工作流已经存在，如想重新添加工作流，请删除原工作流", "workflowid":wfid}
                res = json.dumps(res)
                return res
        #创建脚本文件夹和工作流文件夹
        res1 = self.create_dir(dirName,'develop')
        code1 = json.loads(res1)['code']
        res2 = self.create_dir(dirName,'workflow')
        code2 = json.loads(res2)['code']
        if  code1  not in [200, 409] or code1 not in  [200, 409]: return res1
        logger.info('Successful folder creation')
        #上传脚本文件
        for filePath in filePathList:
            res = self.upload_script(dirName, filePath)
            logger.info(res)
            if json.loads(res.encode('utf-8'))['code'] != 200:
                return res
            logger.info('Upload Success')
            context = json.loads(res.encode('utf-8'))['result']['context']
            scriptName = filePath.split('/')[-1]
            #新建脚本
            res = self.new_dev(scriptName, context, dirName, scriptType)
            res_u = json.loads(res.encode('utf-8'))
            if res_u['code'] == 200:
                if filePath.find(postfix) != -1:
                    scriptName1 = filePath.split('/')[-1]
                    dirid = res_u['result']['dirid']
                    scripid =  res_u['result']['id']
                    logger.info(scripid)

        #新建工作流
        res3 = self.new_workflow(dirName, taskName, des)
        res_w = json.loads(res3.encode('utf-8'))
        if res_w['code'] not in  [200,409]:
            return res3
        if res_w['code'] == 200:
            wid = res_w['result']['id']
            logger.info(wid)
            logger.info('workflow success')
        #像工作流里面添加文件，需要获得脚本的id和工作流的id
        #需要获得脚本的id
        # if json.loads(res3.encode('utf-8'))['code'] == 409:
        #     res_de,res = self.select_dir( taskName, 'develop','.py')
        #     res_wk,res = self.select_dir( taskName, 'workflow', '.py')
        #     if res_de == 0  or res_wk == 0:
        #         return res
        # elif json.loads(res3.encode('utf-8'))['code'] == 200:
        #     res_de,res = self.select_dir(taskName, 'develop','.py')        
        #     if res_de == 0:
        #         return res
        #获取到相关的id以后,保存工作流
        if wid  and scripid:
            res = self.add_script_to_workflow(wid,scripid,'python', scriptName1)
            logger.info(res)
            if json.loads(res.encode('utf-8'))['code'] == 200:
                logger.info("workflowid:"+wid)
                res = self.submit_workflow(node,extimes,wid,scheduleDetail,scheduleType)
                if json.loads(res.encode('utf-8'))['code'] == 200:
                    ssql = "select * from {recordTable} where workflowname = '{taskName}'".format(recordTable = recordTable,taskName=taskName)
                    resData = self.dber.select_sql(ssql)
                    if len(resData) == 0:
                        data = {'workflowname':taskName, 'wfid':wid, 'scriptid':scripid, 'status': 'up'}
                        self.dber.insert_sql(recordTable,data)
                    elif len(resData) == 1:
                        data = {'wfid':wid, 'scriptid':scripid, 'status': 'up'}
                        where = {'workflowname':taskName}
                        self.dber.update_sql(recordTable,data,where)
                    # remsg ={
                    #     "success": True,
                    #     "msg": "新增映射成功",
                    #     "status": "0",
                    #     "Workflowid":wid
                    #     }
                    # return remsg
                    res = json.loads(res.encode('utf-8'))
                    res['Workflowid'] = wid
                    res = json.dumps(res)
                    return res
                else:
                    return res


    #获取任务id：
    def list_job(self,userid):
        data = {
            "sorttype": 0, 
            "userid": userid, 
            "page": 1, 
            "perpage": 100000, 
            "tasktype": ""
        }
        res = self.request_func(data,self.list_job_url)
        return res

    #任务运行脚本启动并获得任务日志id
    def job_runnow(self,wfid, userid):
        data = {
            "id": wfid,
            "userid": userid 
        }
        res = self.request_func(data,self.runnow_url)
        return res
     
    #获取任务目前的运行状态
    def get_job_status(self,wfid,userid):
        res = self.list_job(userid)
        val = json.loads(res.encode('utf-8'))
        if val['code'] == 200:
            allInfo = val['result']
            if len(allInfo) > 0:
                for i in allInfo:
                    if i['id'] == wfid:
                        status = i['status']
                res = {"code": 200,"status":status}
                res = json.dumps(res)
                return res
            else:
                res = {"code": 10003,"result":"请确认此任务是否存在"} 
                res = json.dumps(res)
                return res    
        else:
            return res



    #判断任务运行状态，如果任务处在等待状态，可以重新运行任务
    def wait_runnew(self,wfid, userid):
        #检查任务运行状态
        res = self.get_job_status(wfid, userid)
        val = json.loads(res.encode('utf-8'))
        if val['code'] == 200:
            status = val['status']
            if status == 'WAITING':
                #运行任务
                res = self.job_runnow(wfid, userid)
                return res
        else:
            return res


    #获取任务运行日志并解析日志
    def get_log(self,logId):
        data = {
            "recordid": logId
        }
        res = self.request_func(data,self.get_log_url)
        return res
     #运行任务并返回任务运行状态
    def run_task_status(self,task_id,userid):
        res = self.job_runnow(task_id,userid)
        if json.loads(res.encode('utf-8'))['code'] == 200:
            recordid = res['result']['recordid']
            res_log = self.get_log(recordid)
            if json.loads(res_log.encode('utf-8'))['code'] == 200:
                log = res['result']

    #工作流下线
    def down_workflow(self,wfid):
        data = {
            "ids": [wfid]
        }
        res = self.request_func(data,self.down_url)
        return res
    #已经下线的工作流删除
    def del_down_workflow(self,wfid):
        data = {
            "ids": [wfid],
            "isdel": True
        }
        res = self.request_func(data,self.del_wf_url)
        return res
    #未下线的工作流删除，需要先将工作流下线
    def del_undown_workflow(self,wfid,recordTable):
        #下线
        ssql = "select * from {recordTable} where wfid = '{wfid}'".format(recordTable = recordTable,wfid=wfid)
        resData = self.dber.select_sql(ssql)
        if len(resData) == 1:
            data = {'status': 'down'}
            where = {'wfid':wfid}
            self.dber.update_sql(recordTable,data,where)
        res = self.down_workflow(wfid)
        if json.loads(res.encode('utf-8'))['code'] == 200:
            #删除工作流
            self.del_down_workflow(wfid)
            return res
        else:
            return res

    #停止任务运行
    def stop_job(self,wfid):
        data = {
            "id": wfid,
        }
        res = self.request_func(data,self.stop_url)
        return res        
    
    #请求函数
    def request_func(self,data,url):
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(url, headers = headers, data = data)
        res = response.text
        return res



if __name__ == '__main__':
    dodoxer = OperateDodox()
    #dodoxer.add_dodox('dodox_test',1,"09:30","sh /root/test.sh")
    #dodoxer.create_dir('qingxiangju','access')
    #dodoxer.login_ds('datatom','123456')
    #dodoxer.uplaod_script()
    #dodoxer.new_workflow()
    #dodoxer.create_all_nodes('huanbaoju',['/opt/datatom/dana_api/execute_cfg/huanbaoju_16_87_test_origins_local.py','/opt/datatom/dana_api/execute_cfg/huanbaoju_16_87_test_origins_local.json'], 'huanbaoju_16_87_test_origins_local','环保处_测试数据表','.py','python','172.26.16.90',1,"10min",0,'public.task_info')
    #dodoxer.run_task_status()
    #dodoxer.del_undown_workflow('73d031b7b1f15568c9037c25ecbd6a85')
    #dodoxer.wait_runnew('73d031b7b1f15568c9037c25ecbd6a85','AWqaZmChckUwDRI9nPVk')
    #res = dodoxer.refresh_token()
    #print(res)

