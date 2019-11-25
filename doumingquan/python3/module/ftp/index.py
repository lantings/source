from ftplib import FTP
import os
import datetime
import time
class FTP_OP(object):
    def __init__(self,hostname,username,password,port):
        """
        :param hostname: ftp主机ip
        :param username: ftp用户名
        :param password: ftp密码
        :param port: ftp端口默认21
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port     = port

    def connect(self):
        """
        连接ftp
        :return:ftp连接对象
        """
        ftp = FTP()
        ftp.set_debuglevel(0) #不开启调试模式
        ftp.connect(host=self.host,port=self.port)
        ftp.login(self.username,self.password)
        return ftp

    def download_file(self,ftp_file_path,dst_file_path,temp_ftp_file_name):
        """
从ftp下载文件到本地
        :param ftp_file_path:  ftp文件所在路径
        :param dst_file_path:  本地存放路径
        :param temp_ftp_file_name:
        :return:
        """
        buffer_size = "" #默认8192
        ftp = self.connect()
        print(ftp.welcome())    #显示ftp登陆信息

        file_list = ftp.nlst(ftp_file_path)
        for file_name in file_list:
            with open(dst_file_path) as f:
                ftp.retrbinary('RETR {0}'.format(ftp_file_path), f.write, buffer_size)
