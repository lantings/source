#coding=utf-8

import requests
import json
import hashlib

class OperateDodox():
    def __init__(self):
        self.login_url ="http://172.26.16.90/danastudio/login"
        self.upload_url = "http://172.26.16.90/danastudio/dodox/filemanager/file/upload"
        self.workflow_url = "http://172.26.16.90/danastudio/ants/workflow/new"
    def add_dodox(self,taskName, scheduletype, scheduledetail,cmd):
        url = "http://127.0.0.1:13500/dodox/job/add"
        data = {
            "name": taskName,
            "tasktype": "spark",#使用委办局英文名进行分组
            "exectimes": -1,
            "scheduletype": scheduletype,
            "scheduledetail": scheduledetail,
            "autoassign": False,
            "assignnode": "10.15.8.103",
            "env": ["shell"],
            "userid": "datatom",
            "subjob": [
                {
                    "name": "subtask 1",
                    "subid": 1,
                    "cmd": cmd
                }
              ]}
        data = json.dumps(data)
        res = json.loads(requests.post(url, data).content)
        print(res)

    def md5(self,para):
        m2 = hashlib.md5()
        m2.update(para)
        return m2.hexdigest()

    def create_dir(self,dirName,moduleFlag):
        url= "http://127.0.0.1/danastudio/ants/folder/create"
        data ={
            "dirname":"dashuju333",
            "module":moduleFlag
        }
        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjQ3MTY4NTksImlhdCI6MTU2NDExMjA1OSwiaXNzIjoiZGFuYXN0dWRpb19hdXRoX3NlcnZlciIsIm1vZHVsZXMiOlsiYWNjZXNzIiwiZGV2ZWxvcCIsIndvcmtmbG93IiwidmF1bHQiLCJkZXZjZW50ZXIiLCJvcGVyYXRpbmciXSwicm9sZV9pZCI6ImRldmVsb3BlciIsInJvbGVfbmFtZSI6IuW8gOWPkeiAhSIsInRrdmVyc2lvbiI6MSwidXNlcl9pZCI6IkFXcWFabUNoY2tVd0RSSTluUFZrIiwidXNlcl9uYW1lIjoiZGF0YXRvbSJ9.DJtcXvVjVJ6ozcTx5gwUkB8Sc-Ud_pOyy7VCQugb4cC4eSijix38RWs7MQeGwIzDAwcJENG5sgPTmsW9Rw9lO5ufcdOQC-ReQjlIAVAX5VnuWqv4WgPMX9kY3b_fVIh6-dj8p9EF_5-NVZt0GxcXYPcci-PojjUIrgk9IGqCOeXTuLV4wOYan1xHeQY7GQlZ3l8qMZYbYmp77ab_f47kI-UViX5xiGa18xHmfKSdYfjzl06fJvY4wIaLqUWBgst9zoqAj8Brygxc9NMrexJL7Ly6B68fQmiP7IawVvmaix7XV6pGXe5RY2jtTRADiY2pUkvPj9gpdXBlk79pNKKL9DsyBLXGSRoxC9S3cCIIW3ZGOo9GojPcoJCxFz-rPdLVIT_Kr2qSTD8reQwJIuSRmeqByQwAs1_hd6krdmCcDyfZMLYoQm5dmNDcgRx5T9_vKjwK6o7uAGAzFvqBKiHMwcgXaLBBoL_-5RSZUiqcUSEtpU_1-x9n8RCNN3ALIGmDldjvpw6EcSOha8l4hi4GHQ6wgfPph3Syf8WLS-_8meNNZWrwVUiECszFZSx_ld5fLo590J5RfYrqs1RR5kBLbOmd6DXky9hr-qIrSBjBT0_F2ewvGbScYJMeLWkdznQiLalplvZqrfNLV383PRUGn-IR7g3Utd27Q0NGZj_Ali0"
        }
        data = json.dumps(data)
        #res = requests.post(url, data).
        res = json.loads(requests.post(url,headers = headers, data = data).content)
        print(res)
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

    def uplaod_script(self):

        data = {
            "force": True,
            "absdir":"/var/dana/dodox/filemanager/file/admin/dashuju33322",
            "file": "@/opt/dodox_api/test.sh",
            "trans": True
        }
        headers = {
            "cache-control": "no-cache",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjQ3MTY4NTksImlhdCI6MTU2NDExMjA1OSwiaXNzIjoiZGFuYXN0dWRpb19hdXRoX3NlcnZlciIsIm1vZHVsZXMiOlsiYWNjZXNzIiwiZGV2ZWxvcCIsIndvcmtmbG93IiwidmF1bHQiLCJkZXZjZW50ZXIiLCJvcGVyYXRpbmciXSwicm9sZV9pZCI6ImRldmVsb3BlciIsInJvbGVfbmFtZSI6IuW8gOWPkeiAhSIsInRrdmVyc2lvbiI6MSwidXNlcl9pZCI6IkFXcWFabUNoY2tVd0RSSTluUFZrIiwidXNlcl9uYW1lIjoiZGF0YXRvbSJ9.DJtcXvVjVJ6ozcTx5gwUkB8Sc-Ud_pOyy7VCQugb4cC4eSijix38RWs7MQeGwIzDAwcJENG5sgPTmsW9Rw9lO5ufcdOQC-ReQjlIAVAX5VnuWqv4WgPMX9kY3b_fVIh6-dj8p9EF_5-NVZt0GxcXYPcci-PojjUIrgk9IGqCOeXTuLV4wOYan1xHeQY7GQlZ3l8qMZYbYmp77ab_f47kI-UViX5xiGa18xHmfKSdYfjzl06fJvY4wIaLqUWBgst9zoqAj8Brygxc9NMrexJL7Ly6B68fQmiP7IawVvmaix7XV6pGXe5RY2jtTRADiY2pUkvPj9gpdXBlk79pNKKL9DsyBLXGSRoxC9S3cCIIW3ZGOo9GojPcoJCxFz-rPdLVIT_Kr2qSTD8reQwJIuSRmeqByQwAs1_hd6krdmCcDyfZMLYoQm5dmNDcgRx5T9_vKjwK6o7uAGAzFvqBKiHMwcgXaLBBoL_-5RSZUiqcUSEtpU_1-x9n8RCNN3ALIGmDldjvpw6EcSOha8l4hi4GHQ6wgfPph3Syf8WLS-_8meNNZWrwVUiECszFZSx_ld5fLo590J5RfYrqs1RR5kBLbOmd6DXky9hr-qIrSBjBT0_F2ewvGbScYJMeLWkdznQiLalplvZqrfNLV383PRUGn-IR7g3Utd27Q0NGZj_Ali0"
        }
        data = json.dumps(data)
        res = json.loads(requests.post(self.upload_url,headers = headers, data = data).content)
        #res = requests.post(self.upload_url, headers = headers, data = data).json()
        print(res)

    def new_workflow(self):
        data = {
            "name":"ceshia11",
            "description":"test",
            "tags":[],
            "dirname":"dashuju333",
            "subjob":[
            {
            "subid":1,
            "description":"这是一个子任务的测试",
            "cmd":"sh /opt/dodox_api/test.sh"
            }
            ]
                    }
        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjQ3MTY4NTksImlhdCI6MTU2NDExMjA1OSwiaXNzIjoiZGFuYXN0dWRpb19hdXRoX3NlcnZlciIsIm1vZHVsZXMiOlsiYWNjZXNzIiwiZGV2ZWxvcCIsIndvcmtmbG93IiwidmF1bHQiLCJkZXZjZW50ZXIiLCJvcGVyYXRpbmciXSwicm9sZV9pZCI6ImRldmVsb3BlciIsInJvbGVfbmFtZSI6IuW8gOWPkeiAhSIsInRrdmVyc2lvbiI6MSwidXNlcl9pZCI6IkFXcWFabUNoY2tVd0RSSTluUFZrIiwidXNlcl9uYW1lIjoiZGF0YXRvbSJ9.DJtcXvVjVJ6ozcTx5gwUkB8Sc-Ud_pOyy7VCQugb4cC4eSijix38RWs7MQeGwIzDAwcJENG5sgPTmsW9Rw9lO5ufcdOQC-ReQjlIAVAX5VnuWqv4WgPMX9kY3b_fVIh6-dj8p9EF_5-NVZt0GxcXYPcci-PojjUIrgk9IGqCOeXTuLV4wOYan1xHeQY7GQlZ3l8qMZYbYmp77ab_f47kI-UViX5xiGa18xHmfKSdYfjzl06fJvY4wIaLqUWBgst9zoqAj8Brygxc9NMrexJL7Ly6B68fQmiP7IawVvmaix7XV6pGXe5RY2jtTRADiY2pUkvPj9gpdXBlk79pNKKL9DsyBLXGSRoxC9S3cCIIW3ZGOo9GojPcoJCxFz-rPdLVIT_Kr2qSTD8reQwJIuSRmeqByQwAs1_hd6krdmCcDyfZMLYoQm5dmNDcgRx5T9_vKjwK6o7uAGAzFvqBKiHMwcgXaLBBoL_-5RSZUiqcUSEtpU_1-x9n8RCNN3ALIGmDldjvpw6EcSOha8l4hi4GHQ6wgfPph3Syf8WLS-_8meNNZWrwVUiECszFZSx_ld5fLo590J5RfYrqs1RR5kBLbOmd6DXky9hr-qIrSBjBT0_F2ewvGbScYJMeLWkdznQiLalplvZqrfNLV383PRUGn-IR7g3Utd27Q0NGZj_Ali0"
        }
        data = json.dumps(data)
        res = json.loads(requests.post(self.workflow_url,headers = headers, data = data).content)
        print(res)

if __name__ == '__main__':
    dodoxer = OperateDodox()
    #dodoxer.add_dodox('dodox_test',1,"09:30","sh /root/test.sh")
    #dodoxer.create_dir('qingxiangju','access')
    #dodoxer.login_ds('datatom','123456')
    #dodoxer.uplaod_script()
    dodoxer.new_workflow()
