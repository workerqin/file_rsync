#!/usr/bin/python
#-*-coding:utf-8-*-

import socket

def server():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sk.bind(('119.29.120.47', 8000))
    sk.bind(('10.135.187.20', 8000))
    sk.listen(5)
    while True:
        client, addr = sk.accept()
        data = client.recv(1024)
        print data
        #while 1:
            #client.send('hello')
        #client.close()

if __name__ == "__main__":
    server()
