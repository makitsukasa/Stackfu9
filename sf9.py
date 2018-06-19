# stackfu9 interpreter

import sys, io;
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DEBUG_OUTPUT = False
OUTPUT_AS_CHARACTER = True

# element of the stack
# each element contains bignum
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
		if OUTPUT_AS_CHARACTER:
			if self.n < 10:
				return str(self.n)
			elif self.n == 10:
				return '\n'
			elif self.n < 32:
				return ''
			elif 0xD800 <= self.n <= 0xDFFF: # python do not allow surrogate
				return ''
			elif self.n > 0x1efff:
				return ''
			return chr(self.n)
		else:
			if self.n < 10:
				return str(self.n)
			elif self.n < 32:
				return ''
			elif 0xD800 <= self.n <= 0xDFFF:
				return ''
			elif self.n > 0x1efff:
				return ''
			return chr(self.n)

	def __eq__(self, other):
		return self.asNumber() == other.asNumber()

	def __str__(self):
		if OUTPUT_AS_CHARACTER:
			return self.asCharacter()
		return str(self.asNumber()) + '(' + self.asCharacter() + ')'

# just wrapper of array
# unlimited stack size
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
			# left roll
			self.stack.append(self.stack.pop(len(list) - 1 + depth))
		else:
			# right roll
			self.stack.insert(-depth, self.stack.pop())
		return

	def __str__(self):
		retStr = ''
		for elem in self.stack:
			retStr += str(elem) + ', '
		return retStr

# how each operand works
# @return how many program counter moves
# - jump : any value
# - other : 0
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
	if len(var) == 0:
		stack.push(Element(0))
	else:
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

def execPickedNumber(source):
	source = '00=' + source
	i = 0
	while i < len(source):
		i += opDic[source[i]]() + 1
	return stack.pop().asNumber()

def execute(source):
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
	#DEBUG_OUTPUT = True

	# print Hi
	source = '00=""+"+"++"+"+"+.00=""""++"+"++"+"+"++.'

	# print Hello World!
	_source = '00=""++""++"+"+"+.00="""+"++""+"++"+"++.00=""++""++""++"+"+.00=""++""++""++"+"+.00="""++""++"+"++""++.00="+"+"+"+"+.00="""++"++""+"+"+"++.00="""++""++"+"++""++.00="""++""++"++""++"+.00=""++""++""++"+"+.00=""+"++""+"++"+"+.00=""+"+"+"+"++.'

	# add big number 12345678901234567890 + 13579246801357924680
	_source = '00="""""""""""""++"+"+"+"+"+"+"+"++"+"++""++""++""++""++"+"+"+"+"+"+"++"+"+"+"++""++"++""++"+"++""++""++"++"+"+"+"++""++""++"++""++"+"++""+"++""++"+"++""+"++""++""++"+00="""""""""""+"+"+"+"+"+"+"++""+"++"+"+"+"+"++"+"+"+"++"+"++""++""++"+"+"+"+"++""+"++"++""++""++"+"++""+"++"++"+"+"+"+"+"+"++""++""++""++"+"++""+"++""++""++"+"+"++.'

	# roll test
	_source = '000="00=+"00=+"00=+"00=+00="+%......'

	# print integer
	_source = '00="+""+""+""+""+"+""+""+"+"+""+""+"+"+++++++++.'

	# single loop
	_source = '00=""+"+"+"+"+"++"0=""+"+"+"++""++0+0+0+0+0+0+0+0+0+0+0+0+0+0+^00=-".00="""+"+"+"+"++""++0+0+0+0+0+0+0+0+0+0+0+0+-^'

	# nested loop
	# count down in count down
	_source = '00="+""+"++"0=""+"++""+"++""++"+0+0+0+0+0+0+0+0+0+0+0+0+^""0="""++"+"++"+"+0+0+0+0+0+0+0+0+0+0+0+0+0+0+^".00=-00="""+"+"+"+"++""++0+0+0+0+0+0+0+0+0+0+0+0+-^^00=-00="""""++"+"+"+"++"+"++0+0+0+0+0+0+0+0+0+0+-^^'

	# fizzbuzz
	_source = '000=""+"++""++"+"+"+"0=""+"++""+"++0+^"00=-00=""""+"++"++"+"+-^^"0="""+"+"+"++""+"++"+"+"++0+^000=%"00="0="""""+"++"++"+"+"++"++^0=^00=""++-""0="""++"+"++""++""++0+^""0="""++"+"++""++"+^00=-"0="""++"++"+"+"+^00=%00=+"0=""""++"++""++"++^00=%00="""+"+"+"+"++""++-0+^^"-^00=00=""++^^"-00=""""+"+"+"++""++"++"+-^^0=0="""++"+"++""++"+^00="""++"++""+"++"+.00="""++"++""+"++""++.00="""+"++""++"+"++"+"..00=%00=+00=%"00="0="""+"++""++""++"+"++^0=^00=""+"++-""0="""++"+"++""++""++0+^""0="""++"+"++""++"+^00=-"0="""++"++"+"+"+^00=%00=+"0=""""++"++""++"++^00=%00="""+"+"+"+"++""++-0+^^"-^00=00=""++^^"-00=""""+"+"+"++""++"++"+-^^0=0="""++""++"++"+"+^00=""+"+"+"+"++"+.00="""++"+"++""++""++.00="""+"++""++"+"++"+"..00=%00=+00=%00=%0=0="+^".0=^00="+""+"++.00="""""+"++"++"+"+"++"+"+"+-0+^^'

	# file input output
	source = ',,,...'

	if len(sys.argv) > 1:
		source = open(sys.argv[1]).read()

	execute(source)
