import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        self.write("数据存储在呀")
        self.write("型号")
        res = '172.168.22.156';
        res = res.split('.')
        print(res)

    def post(self):
        self.write("this is post data")


application = tornado.web.Application([
    (r"/test", MainHandler),
])

if __name__ == "__main__":
    application.listen(8800)
    tornado.ioloop.IOLoop.instance().start()