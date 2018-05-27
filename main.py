import sys;

DEBUG_OUTPUT = True

class Element:
	def __init__(self, n):
		if isinstance(n, str):
			if(len(n) == 1):
				self.n = ord(n)
			else:
				print('internal error : long str in Element.constructor')
				sys.exit(1)
		elif isinstance(n, int):
			self.n = n
		elif isinstance(n, Element):
			self.n = n.asNumber()
		else:
			print('internal error : neither int nor char in Element.constructor')
			sys.exit(1)

	def asNumber(self):
		return self.n

	def asCharacter(self):
		if self.n < 32:
			return ''
		return chr(self.n)

	def __eq__(self, other):
		if self.n == other.asNumber():
			return Element(1)
		else:
			return Element(0)

	def __add__(self, other):
		val = self.n + other.asNumber();
		return Element(val);

	def __str__(self):
		return '' + str(self.asNumber()) + '(' + self.asCharacter() + ')'

class Stack:
	def __init__(self):
		self.stack = []

	def push(self, element):
		if not isinstance(element, Element):
			print('internal error : only Element can stack')
			sys.exit(1)
		self.stack.append(element)

	def pop(self):
		if len(self.stack) <= 0:
			if DEBUG_OUTPUT:
				print('runtime error : pop is called but stack is empty')
			else:
				sys.stderr.write('runtime error : pop is called but stack is empty\n')
			sys.exit(1)
		return self.stack.pop(len(self.stack) - 1)

	def roll(self, depth):
		if depth <= 0:
			return
		self.stack.insert(-depth + 1, self.stack.pop())
		return

	def __str__(self):
		retStr = ''
		for elem in self.stack:
			retStr += str(elem) + ', '
		return retStr

def opPushZero():
	stack.push(Element(0))
	return 0

def opAdd():
	y = stack.pop().asNumber()
	x = stack.pop().asNumber()
	stack.push(Element(x + y))
	return 0

def opSubstruct():
	y = stack.pop().asNumber()
	x = stack.pop().asNumber()
	stack.push(Element(x - y))
	return 0

def opDuplicate():
	var = stack.pop()
	stack.push(var)
	stack.push(var)
	return 0

def opEqual():
	y = stack.pop().asNumber()
	x = stack.pop().asNumber()
	ans = 1 if (x == y) else 0
	stack.push(Element(ans))
	return 0

def opInput():
	var = sys.stdin.read(1)
	stack.push(Element(var))
	return 0

def opOutput():
	if DEBUG_OUTPUT:
		print('STDOUT:', end = '')
		#print(stack.pop().asCharacter(), end = '')
		print(stack.pop(), sep = '')
	else:
		#print(stack.pop().asCharacter(), end = '')
		print(stack.pop(), end = '')
	return 0

def opRoll():
	stack.roll(stack.pop().asNumber())
	return 0

def opJump():
	return stack.pop().asNumber()


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

def run(source):
	i = 0
	if DEBUG_OUTPUT:
		while i < len(source):
			print(str(i) + ' : ' + source[i], end = ' ')
			i += opDic[source[i]]() + 1
			print(stack)

	else:
		while i < len(source):
			i += opDic[source[i]]() + 1

	print()

if __name__ == '__main__':
	DEBUG_OUTPUT = False

	# print Hi
	#source = '00=""+"+"++"+"+"+.00=""""++"+"++"+"+"++.'

	# print Hello World!
	#source = '00=""++""++"+"+"+.00="""+"++""+"++"+"++.00=""++""++""++"+"+.00=""++""++""++"+"+.00="""++""++"+"++""++.00="+"+"+"+"+.00="""++"++""+"+"+"++.00="""++""++"+"++""++.00="""++""++"++""++"+.00=""++""++""++"+"+.00=""+"++""+"++"+"+.00=""+"+"+"+"++.'

	# roll test
	#source = '000="00=+"00=+"00=+"00=+00="+"+%......'

	# print integer
	#source = '00="+""+""+""+""+"+""+""+"+"+""+""+"+"+++++++++.'

	# single loop
	#source = '00=""+"+"+"+"+"++"0=""+"+"+"++""++0+0+0+0+0+0+0+0+0+0+0+0+0+0+^00=-".00="""+"+"+"+"++""++0+0+0+0+0+0+0+0+0+0+0+0+-^'

	# nested loop
	# count down in count down
	source = '00="+""+"++"0=""+"++""+"++""++"+0+0+0+0+0+0+0+0+0+0+0+0+^""0="""++"+"++"+"+0+0+0+0+0+0+0+0+0+0+0+0+0+0+^".00=-00="""+"+"+"+"++""++0+0+0+0+0+0+0+0+0+0+0+0+-^^00=-00="""""++"+"+"+"++"+"++0+0+0+0+0+0+0+0+0+0+-^^'

	run(source)
