# s    f 9w        2  s    f 9             .py
# Stackfu9Writable to Stackfu9 interpreter
#
# python sf9w2sf9.py input.sf9w output.sf9

# Stackfu9Writable is a Stackfu9 extension.
# It's sf9 with new sugar syntaxes.
# - '[' jumps past the matching ']' if 0
# - ']' jumps back to the matching '['
# - '<' evaluates to 1 if the stack top is less    than             zero, and otherwise to 0
# - '>' evaluates to 1 if the stack top is greater than             zero, and otherwise to 0
# - '{' evaluates to 1 if the stack top is less    than or equal to zero, and otherwise to 0
# - '}' evaluates to 1 if the stack top is greater than or equal to zero, and otherwise to 0
# - 'character' push immediate value

import linecache
import main
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
	'[',
	']',
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

# @param source that not resolved jumps
# @return source that resolved jumps
#
# loop looks like 'M[N]' => 'M"0=A^NB^'
# - 'M' decides do loop or pass, you may use M as loop counter
# - 'A^' jumps to tail of the loop
# - 'N' is operands in the loop
# - 'B^' jumps to head of the loop
# you may put '^' just after the loop to remove loop counter
#
# '[]' is always 92 operands after parse
def resolveLoop(source):
	i = 0
	ans = []
	while i < len(source):

		if source[i] is ']':
			print("error : ']' detected without '['", i)
			return ""
		if source[i] is not '[':
			ans += source[i]
			i += 1
			continue

		# loop
		ans_in_loop = []
		hoge = i
		i += 1		# ignore '[' once
		while source[i] is not ']':
			if source[i] is '[':
				# loop is nested
				nested_part = []
				nest_depth = 0
				print("nest from", i)
				while True:
					if source[i] is '[':
						print(i, "is '['")
						nest_depth += 1
					elif source[i] is ']':
						print(i, "is ']'")
						nest_depth -= 1
					nested_part += source[i]
					if nest_depth <= 0:
						break
					i += 1

				# now nested_part is like '[00000000]'
				print("nested parts is", ''.join(nested_part))
				ans_in_loop += resolveLoop(nested_part)
			else:
				ans_in_loop += source[i]

			i += 1

			if i >= len(source):
				print("error : ']' is not found after '['", hoge)
				return ""

		# 'M[N]' => 'M"0=A^NB^'
		# i need len(NB^) to decide A
		# i need len("0=A^NB^) to decide B
		# for this problem, i decide both len(A) and len(B) is PICKNUMBER_OVERHEAD
		# but it is not best way
		ans += '"0='
		num = len(ans_in_loop) + PICKNUMBER_OVERHEAD_WITH_HEADER + 1
		ans += list(opImmidiateValue(num,
				header = False, fill = PICKNUMBER_OVERHEAD))
		ans += '^'
		ans += ans_in_loop
		num = -(len(ans_in_loop) + PICKNUMBER_OVERHEAD_WITH_HEADER + PICKNUMBER_OVERHEAD + 5)
		ans += list(opImmidiateValue(num,
				header = True, fill = PICKNUMBER_OVERHEAD))
		ans += '^'
		i += 1

	return ans

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

	print(source_string)
	source = list(source_string)
	source = resolveImmediateValue(source)
	source = resolveCompare(source)
	print(''.join(source))
	source = resolveLoop(source)

	#print(source)
	print(''.join(source))

	main.DEBUG_OUTPUT = False
	main.OUTPUT_AS_CHARACTER = True
	main.execute(source)
