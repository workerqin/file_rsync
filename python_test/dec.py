#-*-coding:utf-8-*-

def dec1(func):
	def dec1_func(a, b):
		print "dec1_func"
		c = func(a, b)
		return c*10
	return dec1_func

@dec1
def test(a, b):
	print "test decorator"
	return a+b

if __name__ == "__main__":
	print test(1,2)
