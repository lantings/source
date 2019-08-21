import tornado.ioloop
import tornado.web
import json
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # self.write("数据存储在呀")
        # self.write("型号")
        # res = '172.168.22.156';
        # res = res.split('.')
        # print(res)
        # 渲染模板
        self.render("test.html")

    def post(self):
        self.write("this is post data")
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        print(res['MappingList']['id'])
        strs=''
        target=''
        for key in res['MappingList']:
            strs+=','+key.strip(',')
            target += ',' + res['MappingList'][key].strip(',')
        print(strs.strip(","))
        print(target.strip(","))
        WorkflowTime = res['WorkflowTime']

        cfg_str = "[info]\n"
        cfg_str += "UnitId=" + res['UnitId'].strip() + "\n"
        cfg_str += "UnitName=" + res['UnitName'].strip() + "\n"
        cfg_str += "SourceTableName=" + res['SourceTableName'].strip() + "\n"
        cfg_str += "PrimaryKey=" + res['PrimaryKey'].strip() + "\n"
        cfg_str += "XinghuanTableName=" + res['XinghuanTableName'].strip() + "\n"
        cfg_str += "XinghuanOrcTableName=" + res['XinghuanOrcTableName'].strip() + "\n"
        cfg_str += "MappingList=" + strs.strip(",") + "\n"
        # cfg_str += "MappingList="+str(','.join(res['MappingList']).encode('utf-8').strip().split(','))+"\n"
        cfg_str += "Exectimes=" + str(res['Exectimes']) + "\n"
        cfg_str += "ScheduleType=" + str(WorkflowTime['ScheduleType']) + "\n"
        cfg_str += "ScheduleDetail=" + WorkflowTime['ScheduleDetail'] + "\n"
        cfg_str += "AddTimefield=" + res['AddTimefield'].strip() + "\n"
        cfg_str += "ColumnType=" + res['ColumnType'].strip()+ "\n"
        cfg_str += "TargetList=" + target.strip(",") + "\n"
        print(cfg_str)


# application = tornado.web.Application([
#     (r"/test", MainHandler),
# ])
# https://www.cnblogs.com/zhanghongfeng/p/8004317.html
# 启动模板
application = tornado.web.Application(handlers=[(r"/test", MainHandler)],template_path=os.path.join(os.path.dirname(__file__),"template"),)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8822)
    tornado.ioloop.IOLoop.instance().start()

# {"UnitId":"765123","UnitName": "huanbaoju","XinghuanAddress": "jdbc:hive2://172.26.41.32:30366/tdt;guardianToken=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH","HttpfsAddress": "http://172.26.41.32:32055/webhdfs/v1/tmp/?op=CREATE&guardian_access_token=6mKYTUMtterzxlYyMpv4-CEIJAZ5.TDH","SourceTableName": "test_canal","XinghuanTableName": "gonganju_txt_ods.base_syrk_t_zp_edz_df","MappingList": ["id","name"],"Exectimes": -1,"WorkflowTime": {"ScheduleType":3,"ScheduleDetail":"10,19:30"},"AddTimefield": "jhpt_update_time","PrimaryKey":"empty","XinghuanOrcTableName":"gonganju_orc_ods.base_syrk_t_zp_edz_df","ColumnType":"date","TargetList": ["id","name"]}






