# s    f 9w        2  s    f 9             .py
# Stackfu9Writable to Stackfu9 interpreter
#
# python sf9w2sf9.py input.sf9w output.sf9

# Stackfu9Writable is a Stackfu9 extension.
# It's sf9 with new sugar syntaxes.
# - '!LABEL_NAME!' jumps to label if non-zero
# - ':LABEL_NAME:' defines label
# - '<' evaluates to 1 if the stack top is less    than             zero, and otherwise to 0
# - '>' evaluates to 1 if the stack top is greater than             zero, and otherwise to 0
# - '{' evaluates to 1 if the stack top is less    than or equal to zero, and otherwise to 0
# - '}' evaluates to 1 if the stack top is greater than or equal to zero, and otherwise to 0
# - 'character' push immediate value

import linecache
import sys
#import main
from pick_number import pickNumber

PICKNUMBER_OFFSET = 285
PICKNUMBER_OVERHEAD = 42
PICKNUMBER_OVERHEAD_WITH_HEADER = PICKNUMBER_OVERHEAD + 3

opListSF9 = [
	'0',
	'+',
	'-',
	'=',
	'"',
	',',
	'.',
	'%',
	'^',
]

opListSF9W = [
	'!',
	':',
	'<', # less than zero
	'>', # greater than zero
	'{', # less than or equal to zero
	'}', # greater than or equal to zero
]

opListSF9WCompare = [
	'<',
	'>',
	'{',
	'}',
]

# bf9 does not follow immidiate value
# pickNumber() to get operand that push val onto stack top
def opImmidiateValue(val, header = True, fill = None):
	if val == 0:
		return '0'

	elif val > 0:
		#target_line = linecache.getline('pick_number.txt', val + PICKNUMBER_OFFSET)
		#target = target_line.split(' ')[-1].strip()
		target = pickNumber(val)

		if fill is not None:
			while len(target) < fill:
				target += '0+'

		if header:
			target = '00=' + target

		return target

	else:
		fill = None if fill is None else fill - 2
		target = '"' + opImmidiateValue(-val + 1, header = False, fill = fill) + '-'

		if header:
			target = '00=' + target

		return target

# @param source that not resolved immidiate values
# @return source that resolved immidiate values
def resolveImmediateValue(source):
	ans = []
	for op in source:
		if op in opListSF9:
			ans += op
		elif op in opListSF9W:
			ans += op
		else: # immidiate value
			ans += opImmidiateValue(ord(op))
	return ans

def opCompare(op):
	IS_ZERO_SKIP_ALL  = '"0="""""+"++"+"+"++"++"++^'
	IS_ZERO_JUMP_TO_1 = '"0=""+"++""+"++""++"+0+0+^'
	IS_POS = '"[00=-"0="""++""++"++"+"+^00=%00=+"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0'
	IS_NEG = '"[00=+"0="""++""++"++"+"+^00=%00=-"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0'

	if op is '<': # less than zero
		return list(IS_ZERO_SKIP_ALL + IS_NEG)
	if op is '>': # greater than zero
		return list(IS_ZERO_SKIP_ALL + IS_POS)
	if op is '{': # less than or equal to zero
		return list(IS_ZERO_JUMP_TO_1 + IS_NEG)
	if op is '}': # greater than or equal to zero
		return list(IS_ZERO_JUMP_TO_1 + IS_POS)

# @param source that not resolved compares
# @return source that resolved compares
#
# a compare operand is always 193 operands after parse
def resolveCompare(source):
	ans = []
	for op in source:
		if op in opListSF9WCompare:
			ans += opCompare(op)
		else:
			ans += op
	return ans

# _!A!_:A:_ => _a^__
# easiest
def resolveOneJumpForward(source):
	pass

# _:B:_!B!_ => __b^_
# use len(b) to determine b
def resolveOneJumpBackward(source):
	pass

# _:B:_!A!_!B!_:A:_ => __a^_b^__
# use len(a)+len(b) to determine b,
# use len(b) to determine a
def resolveOneJumpNested(source):
	pass

# labels are no longer needed
def eraseLabels(source):
	pass

def resolveJump(source):
	before = source
	after = ''
	while before != after:
		while before != after:
			before = after
			after = resolveOneJumpForward(before)
			before = after
			after = resolveOneJumpBackward(before)

		# now there are no jump except _:B:_!A!_!B!_:A:_
		# special treatment needed
		after = resolveOneJumpNested(before)

	return eraseLabels(after)

if __name__ == '__main__':
	# print Hello World!
	#source_string = 'H.e.l.l.o. .w.o.r.l.d.!.\n.'

	# single loop
	#source_string = 'A[00=-".]^D[00="+"+-".]^'
	#source_string = '00="+""+"++[00=-".]^'

	# nested loop
	#source_string = '00="+""+"++["[".00=-]^00=-]^'

	# positive or negative
	#source_string = '00="+"+"+"[00=-"0="""++""++"++"+"+^00=%00=+"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0.'

	# 2<  2>  2{  2}  -1<  -1>  -1{  -1}  0<  0>  0{  0}
	#source_string = '00="+<.00="+>.00="+{.00="+}.00=""+-<.00=""+->.00=""+-{.00=""+-}.0<.0>.0{0+.0}.'

	# single loop
	source_string = '00="+""+"++:A:00=-".!A!'

	# fizzbuzz
	'''
	source_string = \
		'000=""+"++""++"+"+["00=-]^[000=%'\
			'"00=[0=^00=""++-">]^0=0="""++"+"++""++"+^'\
			'00="""++"++""+"++"+.00="""++"++""+"++""++.00="""+"++""++"+"++"+"..00=%00=+00=%'\
			'"00=[0=^00=""+"++-">]^0=0="""++""++"++"+"+^'\
			'00=""+"+"+"+"++"+.00="""++"+"++""++""++.00="""+"++""++"+"++"+"..00=%00=+00=%'\
			'00=%0=0="+^".0=^00="+""+"++.'\
		']^'
	'''

	if len(sys.argv) > 1:
		source_string = open(sys.argv[1]).read()

	#print(source_string)
	source = list(source_string)
	source = resolveImmediateValue(source)
	source = resolveCompare(source)
	#print(''.join(source))
	source = resolveJump(source)

	#print(source)
	#print(''.join(source))

	if len(sys.argv) > 2:
		open(sys.argv[2], 'w').write(''.join(source))

	#main.DEBUG_OUTPUT = False
	#main.OUTPUT_AS_CHARACTER = True
	#main.execute(source)
