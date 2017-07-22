#-*-coding:utf-8-*-
import zmq
import sys
import threading
import time
from watchdog.observers import Observer
from watchdog.events import *
import os
import commands


def dorsync(src_str, rsyncExePath, srcPath, dstPath, rsyncPwFile):
    #os.chdir("E:/cwrsync/rsync_client/")
    print "dorsync " + src_str
    #result = os.system("rsync.exe -vzrtopgu  --delete --progress  /cygdrive/D/test root@192.168.9.209::qin --password-file=/cygdrive/E/cwrsync/rsync_client/rsyncd.password")
    cmd = "%s -vzrtpu --delete --progress %s %s --password-file=%s --exclude='.svn/'" % (rsyncExePath, srcPath, dstPath, rsyncPwFile)
    print cmd
    result = os.system(cmd)
    #print result

#注意:
#1、update没用--delete参数，就是说服务端删除操作不会同步到客户端
#2、updateSrcPath参数的填写	
def update(rsyncExePath, updateSrcPath, updateDstPath, rsyncPwFile):
    #os.chdir("E:/cwrsync/rsync_client/")
    print "update"
    cmd = "%s -vzrtpu --progress %s %s --password-file=%s --exclude='.svn/'"%(rsyncExePath, updateSrcPath, updateDstPath, rsyncPwFile)
    #print cmd
    result = os.system(cmd)
    #result = os.system("rsync.exe -vzrtopgu  --progress  root@119.29.120.47::qin/test/ /cygdrive/D/test --password-file=/cygdrive/E/cwrsync/rsync_client/rsyncd.password")
    print result
	

	
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, rsyncExePath, srcPath, dstPath, rsyncPwFile):
        self.rePath = rsyncExePath
        self.srcPath = srcPath
        self.dstPath = dstPath
        self.rPwFile = rsyncPwFile
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            dorsync("move dir", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path,event.dest_path)
        else:
            dorsync("move file", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path,event.dest_path)
    
    def on_created(self, event):
        if event.is_directory:
            dorsync("created dir", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path)
        else:
            dorsync("created file", self.rePath, self.srcPath, self.dstPath, self.rPwFile)            
            #print(event.src_path)
    
    
    def on_deleted(self, event):
        if event.is_directory:
            dorsync("deleted dir", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path)
        else:
            dorsync("deleted file", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path)

		
    def on_modified(self, event):
        if event.is_directory:
            dorsync("modified dir", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path)
        else:
            dorsync("modified file", self.rePath, self.srcPath, self.dstPath, self.rPwFile)
            #print(event.src_path)

			


def doHandle(rsyncExePath, rsyncPath, srcPath, dstPath, rsyncPwFile):
    observer = Observer()
    event_handler = FileEventHandler(rsyncExePath, srcPath, dstPath, rsyncPwFile)
    observer.schedule(event_handler,rsyncPath,True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
	


class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, clientName, rsyncExePath, updateSrcPath, updateDstPath, rsyncPwFile, serverInfo):
        self.id = clientName
        self.rePath = rsyncExePath
        self.usPath = updateSrcPath
        self.udPath = updateDstPath
        self.rPwFile = rsyncPwFile
        self.serverInfo = serverInfo
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'%s' % self.id
        socket.identity = identity.encode('utf-8')
        #socket.connect('tcp://119.29.120.47:5570')
        socket.connect('tcp://%s'%self.serverInfo)
        print('Client %s started' % (identity))
        #poll = zmq.Poller()
        #poll.register(socket, zmq.POLLIN)
        #reqs = 0
        while True:
            #reqs = reqs + 1
            #print('Req #%d sent..' % (reqs))
            #socket.send_string(u'request #%d' % (reqs))
            #sockets = dict(poll.poll(1000))
            #msg = socket.recv()
            #print msg

            #if socket in sockets:
                msg = socket.recv()
                print msg
                if msg == "1":
                    update(self.rePath, self.usPath, self.udPath, self.rPwFile)

        socket.close()
        context.term()
		
class CheckFileTask(threading.Thread):
    """CheckFileTask"""
    def __init__(self, rsyncExePath, rsyncPath, srcPath, dstPath, rsyncPwFile):
        self.rePath = rsyncExePath
        self.path = rsyncPath
        self.srcPath = srcPath
        self.dstPath = dstPath
        self.rPwFile = rsyncPwFile
        threading.Thread.__init__(self)

    def run(self):
        doHandle(self.rePath, self.path, self.srcPath, self.dstPath, self.rPwFile)
		
def Usage():
    print "python client.py client_name rsync_exe_path rsync_path src_path dst_path update_src_path update_dst_path rsync_pw_file server_info"
	
if __name__ == "__main__":
    #print sys.argv
    args = sys.argv
    if len(args) != 10:
        Useage()
	
    #用户名（必须和服务器/home/目录下的用户名对应）	
    clientName = args[1]
    #rsync的可执行文件位置
    rsyncExePath = args[2]
    #rsync监控的文件目录
    rsyncPath = args[3]
    #rsync指令的src参数，表示源路径
    srcPath = args[4]
    #rsync指令的dst参数，表示目标路径
    dstPath = args[5]
    #rsync指令的src参数，表示客户端主动更新服务端修改的文件的源路径
    updateSrcPath = args[6]
    #rsync指令的src参数，表示客户端主动更新服务端修改的文件的目标路径（和srcPath一样）
    updateDstPath = args[7]
    #rsync指令的本地密码文件路径
    rsyncPwFile = args[8]
    #服务器的ip和端口信息
    serverInfo = args[9]
	
    #rsync服务线程
    check = CheckFileTask(rsyncExePath, rsyncPath, srcPath, dstPath, rsyncPwFile)
    check.start()
    
    #zmq服务线程
    client = ClientTask(clientName, rsyncExePath, updateSrcPath, updateDstPath, rsyncPwFile, serverInfo)
    client.start()
	

	
