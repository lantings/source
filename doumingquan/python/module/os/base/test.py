import os
 
#输出字符串指示正在使用的平台。如果是window 则用'nt'表示，对于Linux/Unix用户，它是'posix'
print(os.name)

#函数得到当前工作目录，即当前Python脚本工作的目录路径
path = os.getcwd()
print(path)

#返回指定目录下的所有文件和目录名
allfile = os.listdir(os.getcwd())
print(allfile)

#删除一个文件
#os.remove()

#运行shell命令
#os.system('cmd')
os.system('ls&&pwd')

#os.path.isfile()和os.path.isdir()函数分别检验给出的路径是一个文件还是目录

wholepath = os.path.abspath('test.py')  # :获得绝对路径
print('--whole path---')
print(wholepath)









