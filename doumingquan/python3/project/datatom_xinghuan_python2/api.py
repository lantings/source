#coding=utf-8

import tornado.ioloop
import tornado.web
import json
import datetime
import ConfigParser
#from GenerateWorkflowScript import source_params
#import jwt
#from check_params import check_params
#from new_createmsyqljson import CreateJson


class add(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world!')
    def post(self):
        res = self.request.body.decode('utf-8')
        #self.write(res)
        res = json.loads(res)
        
        
        self.write(res)
        UnitId = res['UnitId']
        print(UnitId)

        # UnitName = res['UnitName']
        # XinghuanAddress = res['XinghuanAddress']
        # HttpfsAddress = res['HttpfsAddress']
        # SourceTableName = res['SourceTableName']
        # XinghuanTableName = res['XinghuanTableName']
        # MappingList = res['MappingList']
        # Exectimes = res['Exectimes']
        # WorkflowTime = res['WorkflowTime']
        # AddTimefield = res['AddTimefield']
        # unitname,databasetype,sourceip,sourceport,sourcedbname,sourceaddress,sourceusername,sourcepassword = source_params(UnitId)
        # #make conf name
        # ipSplit = sourceip.split('.')
        # tableName = SourceTableName.replace('.','_')
        # confName = "{un}_{ip1}_{ip2}_{tb}.conf".format(un=unitname.lower(), up1= ipSplit[2], ip2=ipSplit[3], tb=tableName.lower())
        # with open('/opt/datatom/dana_api/table_cfg/{cfg}'.format(cfg = confName),'w') as cfgmaker:
        #     cfg_str = "[info]\n"
        #     cfg_str += "UnitId="+res['UnitId'].strip()+"\n"
        #     cfg_str += "UnitName="+res['UnitName'].strip()+"\n"
        #     cfg_str += "XinghuanAddress="+res['XinghuanAddress'].strip()+"\n"
        #     cfg_str += "HttpfsAddress="+res['HttpfsAddress'].strip()+"\n"
        #     cfg_str += "SourceTableName="+res['SourceTableName'].strip()+"\n"
        #     cfg_str += "XinghuanTableName="+res['XinghuanTableName'].strip()+"\n"
        #     cfg_str += "MappingList="+','.join(res['MappingList']).strip()+"\n"
        #     cfg_str += "Exectimes="+res['Exectimes'].strip()+"\n"
        #     cfg_str += "WorkflowTime="+res['WorkflowTime'].strip()+"\n"
        #     cfg_str += "AddTimefield="+res['AddTimefield'].strip()
        #     cfgmaker.write(cfg_str)

        #检查传入的参数格式
        #re_info = check_params(username, passwd, column, table, ip, port, sid,  columnType, timecolumn, operation_flag)
        #if re_info == 1:
            #创建相关配置
        #    res = jsonMaker.touch_para(username, passwd, column, table, ip, port, sid, columnType, timecolumn)
        #    self.write(res)
        #else:
        #    self.write(re_info)

class delete(tornado.web.RequestHandler):
        def post(self):
            table = self.get_body_argument("table")
            ip = self.get_body_argument("ip")
            res = jsonMaker.delete_file(table,ip)
            self.write(res)


application = tornado.web.Application([
    (r"/ds/add", add),
    (r"/ds/delete", delete)
])
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
