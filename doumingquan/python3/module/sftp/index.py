# 链接：https://blog.csdn.net/u014028063/article/details/81197431
#example sshclient
import paramiko
# 实例化一个transport对象
transport = paramiko.Transport(('192.168.199.146', 22))
# 建立连接
transport.connect(username='fishman', password='9')
# 将sshclient的对象的transport指定为以上的transport
ssh = paramiko.SSHClient()
ssh._transport = transport
# 执行命令，和传统方法一样
stdin, stdout, stderr = ssh.exec_command('df')
print (stdout.read().decode())
# 关闭连接
transport.close()


# example sftp
import paramiko
# 实例化一个trans对象# 实例化一个transport对象
transport = paramiko.Transport(('192.168.199.146', 22))
# 建立连接
transport.connect(username='fishman', password='9')
# 实例化一个 sftp对象,指定连接的通道
sftp = paramiko.SFTPClient.from_transport(transport)

# LocalFile.txt 上传至服务器 /home/fishman/test/remote.txt
sftp.put('LocalFile.txt', '/home/fishman/test/remote.txt')
# 将LinuxFile.txt 下载到本地 fromlinux.txt文件中
sftp.get('/home/fishman/test/LinuxFile.txt', 'fromlinux.txt')
transport.close()
