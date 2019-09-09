#coding=utf-8

import requests
import json
import hashlib
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OperateDodox():
    def __init__(self):
        self.login_url ="http://172.26.16.90/danastudio/login"
        self.create_url= "http://127.0.0.1/danastudio/ants/folder/create"
        self.upload_url = "http://172.26.16.90/danastudio/dodox/filemanager/file/upload"
        self.workflow_url = "http://172.26.16.90/danastudio/ants/workflow/new"
        self.script2wf_url = "http://172.26.16.90/danastudio/ants/workflow/save"
        self.listall_url = "http://172.26.16.90/danastudio/ants/folder/list"
        #self.search_url = "http://172.26.16.90/danastudio/ants/develop/search"
        self.submit_url = "http://172.26.16.90/danastudio/ants/workflow/submit"
        self.select_script_url = "http://172.26.16.90/danastudio/ants/"

        self.token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjQ3MTY4NTksImlhdCI6MTU2NDExMjA1OSwiaXNzIjoiZGFuYXN0dWRpb19hdXRoX3NlcnZlciIsIm1vZHVsZXMiOlsiYWNjZXNzIiwiZGV2ZWxvcCIsIndvcmtmbG93IiwidmF1bHQiLCJkZXZjZW50ZXIiLCJvcGVyYXRpbmciXSwicm9sZV9pZCI6ImRldmVsb3BlciIsInJvbGVfbmFtZSI6IuW8gOWPkeiAhSIsInRrdmVyc2lvbiI6MSwidXNlcl9pZCI6IkFXcWFabUNoY2tVd0RSSTluUFZrIiwidXNlcl9uYW1lIjoiZGF0YXRvbSJ9.DJtcXvVjVJ6ozcTx5gwUkB8Sc-Ud_pOyy7VCQugb4cC4eSijix38RWs7MQeGwIzDAwcJENG5sgPTmsW9Rw9lO5ufcdOQC-ReQjlIAVAX5VnuWqv4WgPMX9kY3b_fVIh6-dj8p9EF_5-NVZt0GxcXYPcci-PojjUIrgk9IGqCOeXTuLV4wOYan1xHeQY7GQlZ3l8qMZYbYmp77ab_f47kI-UViX5xiGa18xHmfKSdYfjzl06fJvY4wIaLqUWBgst9zoqAj8Brygxc9NMrexJL7Ly6B68fQmiP7IawVvmaix7XV6pGXe5RY2jtTRADiY2pUkvPj9gpdXBlk79pNKKL9DsyBLXGSRoxC9S3cCIIW3ZGOo9GojPcoJCxFz-rPdLVIT_Kr2qSTD8reQwJIuSRmeqByQwAs1_hd6krdmCcDyfZMLYoQm5dmNDcgRx5T9_vKjwK6o7uAGAzFvqBKiHMwcgXaLBBoL_-5RSZUiqcUSEtpU_1-x9n8RCNN3ALIGmDldjvpw6EcSOha8l4hi4GHQ6wgfPph3Syf8WLS-_8meNNZWrwVUiECszFZSx_ld5fLo590J5RfYrqs1RR5kBLbOmd6DXky9hr-qIrSBjBT0_F2ewvGbScYJMeLWkdznQiLalplvZqrfNLV383PRUGn-IR7g3Utd27Q0NGZj_Ali0"

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
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(self.create_url,headers = headers, data = data)
        res = response.text
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
            print(token)
        else:
            pass



    def refresh_token(self,old_token):
        pass

    #上传脚本文件
    def upload_script(self, dirName, filePath):

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"filepath\"\r\n\r\n/var/dana/dodox/filemanager/file/admin/{dir_name}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"force\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{file_path}\"\r\nContent-Type: false\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(dir_name = dirName, file_path=filePath)
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Authorization': self.token,
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Content-Type': "multipart/form-data; boundary=--------------------------WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Content-Length': "3844",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.post(self.upload_url, data=payload, headers=headers)
        res = response.json()
        return res

    #创建新的工作流
    def new_workflow(self, dirName, taskName, des):
        data = {
            "name": taskName,
            "description": des,
            "tags":[],
            "dirname": taskName
            }
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(self.workflow_url,headers = headers, data = data)
        res = response.text
        print(res)
        return res 

    #获取所有的脚本文件夹
    def get_allDirId(self):
        data = {
            "listall": true,
            "module": "develop"
        }
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(self.listall_url,headers = headers, data = data)
        res = response.json()

    #根据脚本文件夹名称获取脚本名称
    def get_allScript_id(self,dirId):
        data = {
            "dirid": "AWv4oL80BZ1xJXgBM0sb",
            "listall": true,
            "page": 1,
            "perpage": 10000
        }
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(self.search_url,headers = headers, data = data)
        res = response.json()

    #查询文件
    def select_dir(self, keyValue, moduleFlag, postfix):
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
                        if i['notename'] == keyValue+postfix:
                            sid = i['id']
            else:
                if len(res['result']) > 0:
                    for i in res['result']:
                        if i['name'] == keyValue:
                            sid = i['id']
        else:
            sid = 0

        return sid,res
    #保存工作流
    def add_script_to_workflow(self, wfId, scriptId, scriptType,file_name):
        data = {
            "id": wfId,
            "subjob": [{
                "subid": 1,
                "cid": scriptId,
                "ctype": scriptType,    
                "name": file_name,
                "x": 158,
                "y": 119
            }]
        }
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(self.script2wf_url,headers = headers, data = data)
        res = response.text
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
        headers = {
            "Authorization": self.token
        }
        data = json.dumps(data)
        response = requests.post(self.script2wf_url, headers = headers, data = data)
        res = response.text
        return res    
    
    #创建整个工作流
    def create_all_nodes(self, partion, filePathlist,schedul_info, file_name,des):
        #创建脚本文件夹和工作流文件夹
        res1 = self.create_dir(partion,'develop')
        code1 = json.loads(res1)['code']
        res2 = self.create_dir(partion,'workflow')
        code2 = json.loads(res2)['code']
        if  code1  not in [200, 409] or code1 not in  [200, 409]: return res1
        logger.info('Successful folder creation')
        #上传脚本文件
        # for filePath in filePathlist:
        #     res = self.upload_script(partion, filePath)
        #     print(res)
        #     if json.loads(res['code']) != 200:
        #         return res
        # logger.info('Upload Success')
        #新建工作流
        res3 = self.new_workflow(partion,file_name,des)
        if json.loads(res3.encode('utf-8'))['code'] not in  [200,409]:
            return res3
        if json.loads(res3.encode('utf-8'))['code'] == 200:
            wid = json.loads(res3.encode('utf-8'))['result']['id']
        logger.info('workflow success')
        #像工作流里面添加文件，需要获得脚本的id和工作流的id
        #需要获得脚本的id
        if json.loads(res3.encode('utf-8'))['code'] == 409:
            res_de,res = self.select_dir( file_name, 'develop','.py')
            res_wk,res = self.select_dir( file_name, 'workflow', '.py')
            if res_de == 0  or res_wk == 0:
                return res
        elif json.loads(res3.encode('utf-8'))['code'] == 200:
            res_de,res = self.select_dir(file_name, 'develop','.py')        
            if res_de == 0:
                return res
        #获取到相关的id以后,保存工作流
        if res_de  and res_wk:
            res = self.add_script_to_workflow(res_wk,res_de,'python',file_name)
            print(res)
            if json.loads(res.encode('utf-8'))['code'] == 200:
                print(res_wk)
                res = self.submit_workflow("172.26.16.90",1,res_wk,"10min",0)
                print(res)


if __name__ == '__main__':
    dodoxer = OperateDodox()
    #dodoxer.add_dodox('dodox_test',1,"09:30","sh /root/test.sh")
    #dodoxer.create_dir('qingxiangju','access')
    #dodoxer.login_ds('datatom','123456')
    #dodoxer.uplaod_script()
    #dodoxer.new_workflow()
    dodoxer.create_all_nodes('minzhengju',[ '/opt/datatom/script/huanbaoju/huanbaoju_16_87_test_origins_local.py'], 1,'upload','only test')