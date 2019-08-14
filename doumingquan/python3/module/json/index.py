import json
data = {
            "username": "mingquan",
            "password": '123456'
        }
# 字典类型和json的区别 json强制双引号，dict都可以
#     字典转化成json
datas = json.dumps(data)
print(data)
print(data['username'])
print(datas)

# loads()将json对象转化成python对象
info = json.loads(datas)
print(info['password'])

