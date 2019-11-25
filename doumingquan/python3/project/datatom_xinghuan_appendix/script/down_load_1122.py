#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ftplib import FTP
import os
import time
import binascii
import psycopg2

# from get_pic_from_unitname import get_table_count
now_time = time.strftime("%Y%m%d", time.localtime())
ftp = FTP()
# 文件下载路径
pic_unitname_path = "/opt/datatom/dana_appendix_api/appendix/"
data_unitname_path = "/opt/datatom/dana_appendix_api/data_appendix/"


def connect_ftp(ftpip, ftpport, ftpuser, ftppasswd):
    ftp.connect(host=ftpip, port=ftpport)
    ftp.login(user=ftpuser, passwd=ftppasswd)
    print("login succeed")


def upload_ftp(ftpip, ftpport, ftpuser, ftppasswd, filepath, unitname,sourcetablename):


 # 取出系统当前时间即最大时间
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    todays = time.strptime(today, "%Y-%m-%d")
    # todaytime = int(time.mktime(todays))
    todaytime = int(time.mktime(time.localtime()))
    connect_ftp(ftpip, ftpport, ftpuser, ftppasswd)
    x = ftp.nlst(filepath)

    data_unitname = pic_unitname_path + unitname + '/' + sourcetablename.split('.')[0] + '_' + sourcetablename.split('.')[1] + '/' + sourcetablename.split('.')[0] + '_' + sourcetablename.split('.')[1] + '_' + now_time
    if os.path.exists(data_unitname) == False:
        os.system("mkdir -p %s"%data_unitname)
    else:
        print("weibanju dirname is already created")
    lists = []

# 不存在即建文件，导出所有数据并把当前时间记录到maxtime_path
    conn = psycopg2.connect(database="postgres",user="stork",password="stork",host="172.27.148.53",port="14103")
    cursor = conn.cursor()


    sql = "select maxtime from public.max_time"
    cursor.execute(sql)
    row = cursor.fetchall()
    print(row)
    if row == []:
        cursor.execute("insert into public.max_time values ('%s')"%todaytime)
        flag = 1
    else:
        flag = 0

    # if os.path.exists(maxtime_path) == False:
    #     flag = 1
    #     os.system("touch %s"%maxtime_path)
    #     print("maxtime_path is not exist,download all files")
    # else:
    #     print("maxtime_path is already exist,get maxtime to download file between maxtime and now")
    #     flag = 0

    ftp_max_timesatmp = []

    if flag==1:
        for i in range(len(x)):
            print(x[i])
            pic = x[i].split("/")[-1]
            # 获取文件时间
            L = list(ftp.sendcmd('MDTM ' + "%s" % x[i]))
            dir_t = L[4] + L[5] + L[6] + L[7] + '-' + L[8] + L[9] + '-' + L[10] + L[11] + ' ' + L[12] + L[13] + ':' + L[14] + L[15] + ':' + L[16] + L[17]
            timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
            # 文件时间,总是差8小时
            timestamp = int(time.mktime(timeArray)) + 28800
            # commontime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            timeArray = time.localtime(timestamp)
            commontime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            with open(data_unitname + "/" + pic, "wb") as f:
                ftp.retrbinary('RETR ' + filepath + "/" + pic, f.write)
            f.close()

            #将文件转换成16进制
            fh = open(data_unitname + "/" + pic, "rb")
            a = fh.read()
            hexstr = binascii.hexlify(a)
             # 将数据放入list
            b = {'name': pic, 'time': commontime, 'binary': hexstr}
            lists.append(b)
            ftp_max_timesatmp.append(timestamp)

    else:
        # # 获取最大时间
        # with open(maxtime_path,'rb') as n:
        #     t = n.readlines()
        # n.close()
        maxtime = int(row[0][0])
        print(maxtime)

        #maxtime = int(t[-1].split("\n")[0])
        for i in range(len(x)):
            pic = x[i].split("/")[-1]
            # 获取原文件时间
            L = list(ftp.sendcmd('MDTM ' + "%s" % x[i]))
            dir_t = L[4] + L[5] + L[6] + L[7] + '-' + L[8] + L[9] + '-' + L[10] + L[11] + ' ' + L[12] + L[13] + ':' + L[14] + L[15] + ':' + L[16] + L[17]
            timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
            # 文件时间,总是差8小时
            timestamp = int(time.mktime(timeArray)) + 28800

            # commontime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            timeArray = time.localtime(timestamp)
            commontime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            
     #   print(max(ftp_max_timesatmp))

   #     for i in range(len(x)):
            if maxtime < timestamp:
        # 文件下载
                print("when maxtime<timestamp maxtime is ",maxtime,"timestamp value is :",timestamp)
                with open(data_unitname + "/" + pic, "wb") as f:
                    ftp.retrbinary('RETR ' + filepath + "/" + pic, f.write)
                f.close()
                # 将文件转换成16进制
                fh = open(data_unitname + "/" + pic, "rb")
                a = fh.read()
                hexstr = binascii.hexlify(a)
                # 将数据放入list
                b = {'name': pic, 'time': commontime, 'binary': hexstr}
                lists.append(b)

            ftp_max_timesatmp.append(timestamp)
        print(max(ftp_max_timesatmp))

    #写入maxtime时间
    if len(lists):
        print(todaytime)
        sql = "update public.max_time set maxtime = '%s'"%(str(max(ftp_max_timesatmp)))
        print(sql)
        cursor_update = conn.cursor()
        cursor_update.execute(sql)
        conn.commit()
        # with open(maxtime_path, 'wb') as w:
        #     t = w.write(str(todaytime)+"\n")
        # w.close()
    else:
        print("cannot get any file ,donot update maxtime,return false")
        return False
        
    cursor.close()
    cursor_update.close()
    conn.close()

    strs = ''

    for i in lists:
        strs += i['name'] + "\x01" + i['time'] + "\x01" + i['binary'] + "\n"
    # 生成保存数据的文件
    new_unitname_path = data_unitname_path + unitname + '/' + sourcetablename.split('.')[0] + '_' + sourcetablename.split('.')[1]
    if os.path.exists(new_unitname_path) == False:
        os.system("mkdir -p %s"%new_unitname_path)
    else:
        print("weibanju dirname is already created")
    destpath = new_unitname_path + '/' + sourcetablename.split('.')[0] + '_' + sourcetablename.split('.')[1] + '.txt'
    with open(destpath, 'wb') as z:
        z.write(strs)
    z.close()
    return True


if __name__ == '__main__':
    res = upload_ftp('172.26.16.89', 21, 'detuoftp', 'detuoftp', '/opt/datatom/ftpdata/', 'huanbaoju','test.test1')
    print(res)