#!/usr/bin/python
#-*- coding:utf-8 -*-

class Singleton(object):
    '''单例1 实例id一样, 字典共享'''
    def __new__(cls, *args, **kwargs):
        print args
        print kwargs
    #def __new__(cls, name, bases, attrs):
        if not hasattr(cls, '_inst'):
            #cls._inst = super(Singleton, cls).__new__(cls, names, base, attrs)
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst 

class Borg(type):
	'''单例2 实例id不同，字典共享'''
	_shared_state = {}
	def __new__(cls, *args, **kwargs):
		obj = super(Borg, cls).__new__(cls, *args, **kwargs)
		obj.__dict__ = cls._shared_state	
		return obj

class AuthorTag(type):
    def __new__(cls,  names, base, attrs):
        print names, base, attrs
        attrs['__author__'] = 'jone'
        return super(AuthorTag, cls).__new__(cls, names, base, attrs)

class MyBlog(object):
    __metaclass__ = AuthorTag

def test1():
    class A(Singleton):
        def __init__(self, s):
            self.s = s
	
    a = A('apple')
	#b = A('banana')
    #print id(a),a.s
	#print id(b),b.s

def test2():
	class Example(Borg):
		def __init__(self, *args, **kwargs):
			self.status = 0
	
	a = Example()
	a.status = 1
	b = Example()
	b.status = 2
	print id(a), a.status, id(b), b.status

	

if __name__ == "__main__":
    test = MyBlog()
    print test.__author__
