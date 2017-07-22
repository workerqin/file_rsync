#!/usr/bin/python
#-*-coding:utf-8-*-

from threading import Thread, Condition
import time
import random
from Queue import Queue

#queue = []
#MAX_SIZE = 10
#condition = Condition()
#
#class ProducerThread(Thread):
#    def run(self):
#        nums = range(5)
#        global queue 
#        while True:
#            condition.acquire()
#            if len(queue) == MAX_SIZE:
#                print "queue is full"
#                condition.wait()
#            else:
#                num = random.choice(nums)
#                queue.append(num)
#                print "product %d"%(num)
#                condition.notify()
#            condition.release()
#            time.sleep(random.random())
#
#class ConsumerThread(Thread):
#    def run(self):
#        global queue
#        while True:
#            condition.acquire()
#            if len(queue) <= 0:
#                print "queue is null"
#                condition.wait()
#            else:
#                num = queue.pop(0) 
#                print "consume %d"%(num)
#                condition.notify()
#            condition.release()
#            time.sleep(random.random())




'''
Python Queue模块有三种队列及构造函数:
1、Python Queue模块的FIFO队列先进先出。 class Queue.Queue(maxsize)
2、LIFO类似于堆，即先进后出。 class Queue.LifoQueue(maxsize)
3、还有一种是优先级队列级别越低越先出来。 class Queue.PriorityQueue(maxsize)

q.qsize() 返回队列的大小
q.empty() 如果队列为空，返回True,反之False
q.full() 如果队列满了，返回True,反之False
q.full 与 maxsize 大小对应
q.get([block[, timeout]]) 获取队列，timeout等待时间
q.get_nowait() 相当q.get(False)
非阻塞 q.put(item) 写入队列，timeout等待时间
q.put_nowait(item) 相当q.put(item, False)
q.task_done() 在完成一项工作之后，q.task_done() 函数向任务已经完成的队列发送一个信号
q.join() 实际上意味着等到队列为空，再执行别的操作
'''

queue = Queue(3)

class ProducerThread(Thread):
    def run(self):
        nums = range(5)
        global queue
        while True:
            num = random.choice(nums)
            queue.put(num)
            print "product num :%d"%(num)
            print "product size :%d"%(queue.qsize())
            time.sleep(random.random())

class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            num = queue.get()
            queue.task_done()
            print "consume num : %d"%(num)
            print "consume size :%d"%(queue.qsize())
            time.sleep(random.random())


if __name__ == "__main__":
    ProducerThread().start()
    ConsumerThread().start() 
