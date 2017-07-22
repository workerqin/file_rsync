#!/usr/bin/python
#-*-coding:utf-8-*-

import socket

def client():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sk.connect(('119.29.120.47', 8213))
    sk.connect(('127.0.0.1', 8000))
    #sk.send("hello server")
    #data = sk.recv(1024)
    #print data
    sk.send("qin")
    sk.close()
    #if len(data) >= 0:
    #    sk.close()
    #    break
    

if __name__ == "__main__":
    client() 
