#-*-coding:utf-8-*-
import zmq
import sys
import threading
import time
from watchdog.observers import Observer
from watchdog.events import *
import os

#监听目录
listenDirs = ["/home",]

#客户端标识
clientIds = []


def doHandleSrc(file):
    keys = file.split("/")
    ident = keys[2]
    if ident not in clientIds:
        clientIds.append(ident)
    #print "doHandleSrc"
    #print ident 

#class FileEventHandler(FileSystemEventHandler):
class FileEventHandler(PatternMatchingEventHandler):
    def __init__(self):
        #FileSystemEventHandler.__init__(self)
        #只对lua文件进行监听
        PatternMatchingEventHandler.__init__(self, patterns=["*.lua"], ignore_patterns=[])

    def on_moved(self, event):
        pass
        #print "move file"
        #if event.is_directory:
        #    print(event.src_path,event.dest_path)
        #else:
        #    print(event.src_path,event.dest_path)

    def on_created(self, event):
        pass
        #print "create file"
        #
        #if event.is_directory:
        #    print(event.src_path)
        #else:
        #    print(event.src_path)

    def on_deleted(self, event):
        print "delete file"
        doHandleSrc(event.src_path)
        #if event.is_directory:
        #    print(event.src_path)
        #else:
        #    print(event.src_path)

    def on_modified(self, event):
        print "modify file"
	#print event.src_path
        doHandleSrc(event.src_path)
        #if event.is_directory:
        #    print(event.src_path)
        #else:
        #    print(event.src_path)
        #    print("-----------")
            

def doHandle():
    observer = Observer()
    event_handler = FileEventHandler()
    for ld in listenDirs:
        observer.schedule(event_handler,ld,True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 


class CheckFileTask(threading.Thread):
    """CheckFileTask"""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        doHandle() 
 

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(5):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        print('Worker started')

        while True:
            for ide in clientIds:
                print ide 
                worker.send_multipart([ide, "1"])
                clientIds.remove(ide)
            
            #ident, msg = worker.recv_multipart()
            #print('Worker received %s from %s' % (msg, ident))
            time.sleep(5)
            #worker.send_multipart([ident, msg])

        worker.close()


if __name__ == "__main__":
    #zmq线程
    server = ServerTask()
    server.start()
    
    #watchdog线程
    check = CheckFileTask()
    check.start()
