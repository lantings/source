import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # self.write("数据存储在呀")
        # self.write("型号")
        # res = '172.168.22.156';
        # res = res.split('.')
        # print(res)
        res=self.request.body.decode('utf-8')
        res = self.get_arguments('name')
        # res=json.load(res)
        print(res)

    def post(self):
        res = self.request.body.decode('utf-8')
        res = json.loads(res)
        # print(res)
        field = res["Field"]

        print("this is field 字段",field)

        a = sorted(field, key=lambda x: x['column_order'])
        # field.sort(key=lambda field:field[3])
        print("sort之后的建表语句",a)

        list=[]
        for i in field:
            data =  i['column_name']+" "+i['column_type']+" comment '"+i['column_desc']+"',"
            # print(data)
            list.append(data)
        str=''
        for i in list:
            str+=i
            print(i)
            # print(list[i])

        print("++++++++++++++",str)
        str = str.rstrip(",")
        print("-------------", str)
        # self.write("this is post data")
        create= "create table xinghuan_orc.tablesname("+str+")"
        # print(create)
#       cd web/tornado/application1
#       python test.py


application = tornado.web.Application([
    (r"/test", MainHandler),
])

if __name__ == "__main__":
    application.listen(8833)
    tornado.ioloop.IOLoop.instance().start()