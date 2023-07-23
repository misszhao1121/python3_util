import cv2
import pyautogui
import numpy as np
import datetime
import os,sys,paramiko,socket
class ssh_info_list():        
    def ssh_info():
        hostname = input("输入服务器ip")
        port = input("请输入服务器端口")
        username = input("输入服务器用户")
        password = input("输入服务器密码")
        info  = [hostname,port,username,password]
        return info
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
def for_ssh():
    paramiko.util.log_to_file('paramiko.log')
    info = ssh_info_list.ssh_info()
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname= info[0],port = int(info[1]),username=info[2],password=info[3])
    command = input("请输入需要执行的命令")
    stdin,stdout,stderr=s.exec_command(command)
    sftp = paramiko.SFTPClient.from_transport(s)
    remotepath = '/tmp/paramiko.log'
    localpath = 'paramiko.log'
    print(stdout.readlines())
    sftp.put(localpath,remotepath)
    s.close

def sftp_ssh():
    t = paramiko.Transport((info[0],info[1]))
    info = ssh_info_list.ssh_info()
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
def dowload_files():
    #!/usr/bin/python
    #coding:utf-8
    info = ssh_info_list.ssh_info()
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

if __name__ == '__main__':
    # xh = ['auto_screen()','dowload_files()']
    # xh2 = input('请选择你要执行的步骤:\n'
    #            '1、auto_screen')
    dowload_files()