import sys;

class Number:
	def __init__(self, n):
		if isinstance(n, str):
			if(len(n) == 1):
				self.n = ord(n)
			else:
				print("internal error")
				sys.exit(1)
		elif isinstance(n, int):
			self.n = n
		else:
			print("internal error")
			sys.exit(1)

	def asInteger(self):
		return self.n

	def asCharacter(self):
		if self.n < 32:
			return ""
		return chr(self.n)

	def __eq__(self, other):
		if self.n == other.asInteger():
			return Number(1)
		else:
			return Number(0)

	def __add__(self, other):
		val = self.n + other.asInteger();
		return Number(val);

class Stack:
	def __init__(self):
		self.stack = []

	def push(self, number):
		if not isinstance(number, Number):
			print("error : only Number can stack")
			sys.exit(1)
		self.stack.append(number)

	def pop(self):
		if len(self.stack) <= 0:
			print("error : stack is empty")
			sys.exit(1)
		return self.stack.pop(len(self.stack) - 1)

	def __str__(self):
		retStr = ""
		for elem in self.stack:
			retStr += "" + str(elem.asInteger()) + "(" + elem.asCharacter() + "), "
		return retStr

def opPushZero():
	stack.push(Number(0))
	return 0

def opAdd():
	x = stack.pop()
	y = stack.pop()
	stack.push(x + y)
	return 0

def opSubstruct():
	x = stack.pop()
	y = stack.pop()
	stack.push(x + y)
	return 0

def opDuplicate():
	var = stack.pop()
	stack.push(var)
	stack.push(var)
	return 0

def opEqual():
	x = stack.pop()
	y = stack.pop()
	stack.push(x == y)
	return 0

def opInput():
	var = sys.stdin.read(1)
	stack.push(Number(var))
	return 0

def opOutput():
	print(stack.pop().asCharacter(), end = "")
	return 0

def opRoll():
	# TODO
	return 0

def opJump():
	return stack.pop().asInteger()


opDic = {
	'0' : opPushZero,
	'+' : opAdd,
	'-' : opSubstruct,
	'=' : opEqual,
	'"' : opDuplicate,
	',' : opInput,
	'.' : opOutput,
	'%' : opRoll,
	'^' : opJump,
}

stack = Stack()

if __name__ == '__main__':
	source = '00=""+"+"++"+"+"+.00=""""++"+"++"+"+"++.'

	i = 0
	while i < len(source):
		print(str(i), ":", source[i], "", end = "")
		i += opDic[source[i]]() + 1
		print(stack)
	print()
