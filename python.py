from __future__ import print_function
from __future__ import unicode_literals
import cv2
import pyautogui
import numpy as np
import datetime
import configparser
import os,sys,paramiko,socket
from paramiko import SSHClient
from ssh_utilk import  *
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory


class Conf:
	# 1. 对象初始化
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.f = os.path.join(self.root_path + "\conf\ssh.conf")
        # print(self.f)
        self.conf.read(self.f)
	# 2. 获取所有的sections
    def read_sections(self):
        print(f"1、获取所有的sections:{self.conf.sections()}")
	# 3. 获取所有的sections对应的options
    def read_options(self, s1):
        print(f"2、获取mysqldb所有的options:{self.conf.options(s1)}")
        # print(f"3、获取mailinfo所有的options:{self.conf.options(s2)}")
    def read_conf(self, m, n):
        name = self.conf.get(m, n)  # 获取指定section的option值
        return  name
        # print(f"4、获取指定section:{m}下的option：{n}的值为{name}")


# class ssh_info_list():
    def ssh_info(self,h,p,u,s):
        hostname = h
        port = p
        username = u
        password = s
        info  = [hostname,port,username,password]
        print(info)
#自动截图并保存在当前可执行文件的img目录下
    def auto_screen():
        print("------------开始截图------------")
        img = pyautogui.screenshot(region=[0, 0, 2500 ,1600])
        #分别代表：左上角坐标，宽高
        #对获取的图片转换成二维矩阵形式，后再将RGB转成BGR
        #因为imshow,默认通道顺序是BGR，而pyautogui默认是RGB所以要转换一下，不然会有点问题
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        curr_time = datetime.datetime.now()   #获取当前时间
        #时间转换成年月日格式
        #去除字符串空格,替换:号为-
        imgname = str(datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')).replace(" ", "") + ".jpg"
        pwdpath = sys.path[0].replace("\\","/") + "/img/"
        filename = pwdpath + imgname.replace(":","-")
        if os.path.exists(pwdpath):
            print("当前截图保存目录是:" + pwdpath)
        else:
            os.makedirs(pwdpath)
            print(pwdpath + "目录已创建")
        print("截图成功，文件名:" + filename)
        print(cv2.imwrite(filename,img))
        cv2.destroyAllWindows()
        print("------------截图完成------------")
    # while 1:
    #     screen()

    #ssh
    def for_ssh(self,info):
        paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        # s = paramiko.SSHClient()
        # s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print(info[0],info[1],info[2],info[3])
        # s.connect(hostname= info[0],port = int(info[1]),username=info[2],password=info[3],timeout=2)
        s.connect(hostname= self.info[0],port = int(self.info[1]),username=self.info[2],password=self.info[3],timeout=2)
        command = input("请输入需要执行的命令")
        stdin,stdout,stderr=s.exec_command(command)
        print(stdin,stdout,stderr)
        sftp = paramiko.SFTPClient.from_transport(s)
        remotepath = '/tmp/paramiko.log'
        localpath = 'paramiko.log'
        print(stdout.readlines())
        sftp.put(localpath,remotepath)
        s.close

    def sftp_ssh(self,info):
        t = paramiko.Transport((info[0],info[1]))
        ssh = paramiko.SSHClient()
        ssh.connect(hostname= info[0],port = int(info[1]),username=info[2],password=info[3])
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath='/tmp/test.txt'
        localpath='/tmp/test.txt'
        sftp.get(remotepath, localpath)
        t.close()
    def commonds_ssh():
        #coding:utf-8
        sys.stderr = open('/dev/null') # Silence silly warnings from paramiko<br>import paramiko as pm
        sys.stderr = sys.__stderr__
        class AllowAllKeys(pm.MissingHostKeyPolicy):
            def missing_host_key(self, client, hostname, key):
                return
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
            client.set_missing_host_key_policy(AllowAllKeys())
            client.connect(hostname=hostname,port = int(port),username=username,password=password)
            channel = client.invoke_shell()
            stdin = channel.makefile('wb')
            stdout = channel.makefile('rb')
            stdin.write('''cd tmpls exit''')
            print(stdout.read())
            stdout.close()
            stdin.close()
            client.close()
#sftp下载指定目录的文件
    def dowload_files(info):
        #!/usr/bin/python
        #coding:utf-8
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname= info[0],port = int(info[1]),username=info[2],password=info[3])

        apath = '/var/log'
        apattern = '"*.log"'
        rawcommand = 'find {path} -name {pattern}'
        command = rawcommand.format(path=apath, pattern=apattern)
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout,stdin,stderr)
        pwdpath = sys.path[0].replace("\\","/") + "/img/"
        filelist = stdout.read().splitlines()
        ftp = ssh.open_sftp()
        for afile in filelist:
            (head, filename) = os.path.split(afile)
            ftp.get(afile, pwdpath + str(filename).replace("b'",'').replace("'",''))
            print(head)
        ftp.close()
        ssh.close()
# dowload_files()
if __name__ == '__main__':
    def exect_command(m):
        ss = Conf()
        command = [m, '\n','\n']
        info = [ss.read_conf('ssh_info','ip'),ss.read_conf('ssh_info','port'),ss.read_conf('ssh_info','user'),ss.read_conf('ssh_info','password')]
        sshClass = SSH_Class(hostIP=info[0], TCP_Port=info[1],userName=info[2], passWord=info[3])
        sshObject = sshClass.connectByPassword()
        result = sshClass.executeSshCommands(sshObject, command)
        print(result)
    # exect_command(input("输入命令"))

    while True:
        com = input("输入命令\n")
        # com1 = prompt('>>>', history=FileHistory('history.txt'))
        if com.lower() == 'quit':
            sys.exit()
        else:
            exect_command(com)