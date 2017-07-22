#-*-coding:utf-8-*-
import time
import zmq

if __name__ == "__main__":

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://10.135.187.20:5555")
    
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)
    
        #  Do some 'work'
        time.sleep(1)
    
        #  Send reply back to client
        socket.send(b"World")
