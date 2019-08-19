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


# application = tornado.web.Application([
#     (r"/test", MainHandler),
# ])
# https://www.cnblogs.com/zhanghongfeng/p/8004317.html
application = tornado.web.Application(handlers=[(r"/test", MainHandler)],template_path=os.path.join(os.path.dirname(__file__),"template"),)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8822)
    tornado.ioloop.IOLoop.instance().start()