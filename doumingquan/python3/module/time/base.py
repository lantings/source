import time
#url:https://www.cnblogs.com/wf-linux/archive/2018/08/01/9400354.html
floats = time.time()
print(floats)
#1565266709.295498


mk = time.mktime(time.localtime())
print(int(mk))
#1565266709.0

local = time.localtime()
print(local)
locals = time.localtime(time.time())
print(locals)

classic = time.strftime("%Y-%m-%d %X",time.localtime())
classic = time.strftime("%Y%m%d ",time.localtime())
print("this is classic time",classic)
#2019-08-08 20:21:25

#生成固定格式的时间表示格式
asc = time.asctime(time.localtime())
asctime = time.ctime(time.time())
print(asc)
print(asctime)
# Thu Aug  8 20:23:47 2019

m = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))[0:8]
print('this is today date '+m)




