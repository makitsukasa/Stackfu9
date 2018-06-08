# s    f 9w        2  s    f 9             .py
# Stackfu9Writable to Stackfu9 interpreter
#
# python sf9w2sf9.py input.sf9w output.sf9

# Stackfu9Writable is a Stackfu9 extension.
# It's sf9 with new sugar syntaxes.
# - '!LABEL_NAME!' jumps to label if zero
# - ':LABEL_NAME:' defines label
# - '<' evaluates to 1 if the stack top is less    than             zero, and otherwise to 0
# - '>' evaluates to 1 if the stack top is greater than             zero, and otherwise to 0
# - '{' evaluates to 1 if the stack top is less    than or equal to zero, and otherwise to 0
# - '}' evaluates to 1 if the stack top is greater than or equal to zero, and otherwise to 0
# - 'character' push immediate value

import linecache
import sys
import re
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

# __p__:B:__q__!B!__r__ => __p__:B:__q__b^__r__
# @param val is len(q)
# @return b
def opImmidiateValueBack(val):
	b = val
	op_b = opImmidiateValue(-val, header = False)
	len_b = len(op_b)
	while b < len_b + val:
		b += 2
		op_b = opImmidiateValue(-b, header = False)
		len_b = len(op_b)

	op_b = opImmidiateValue(-b, header = False, fill = b - len_b)
	#print(b)
	return op_b

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

def get_source_length(source):
	if '!' in source:
		return None

	source_without_label_list = re.split(':[^:]+:', source)
	return len(''.join(source_without_label_list))

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

# __p__!F!__q__:F:__r__ => __p__0=f^__q__:F:__r__
# easiest
def resolveOneJumpForward(source):
	source_string = ''
	if type(source) == list:
		source_string = ''.join(source)
	elif type(source) == str:
		source_string = source
		source = list(source)

	source_splitted = source_string.split('!', 2)
	if len(source_splitted) < 3:
		return source
	p, label_name, q_label_r = source_splitted

	q_label_r_splitted = q_label_r.split(':' + label_name + ':', 1)
	if len(q_label_r_splitted) < 2:
		return source
	q, r = q_label_r_splitted

	length = get_source_length(q)
	if length is None:
		return source

	ans = p + '0=' + opImmidiateValue(length, header = False) + '^' +\
			q + ':' + label_name + ':' + r

	return list(ans)

# __p__:B:__q__!B!__r__ => __p__:B:__q__0=b^__r__
# use len(b) to determine b
def resolveOneJumpBackward(source):
	source_string = ''
	if type(source) == list:
		source_string = ''.join(source)
	elif type(source) == str:
		source_string = source
		source = list(source)

	source_splitted = source_string.split('!', 2)
	if len(source_splitted) < 3:
		return source
	p_label_q, label_name, r = source_splitted

	p_label_q_splitted = p_label_q.rsplit(':' + label_name + ':', 1)
	if len(p_label_q_splitted) < 2:
		return source
	p, q = p_label_q_splitted

	len_q = get_source_length(q)
	if len_q is None:
		return source

	ans = p + ':' + label_name + ':' + q +\
			'0=' + opImmidiateValueBack(len_q + 3) + '^' + r

	return list(ans)

# __p__:B:__q__!F!__r__!B!__s__:F:__t__ => __p__:B:__q__0=f^__r__0=b^__s__:F:__t__
# use len(f) + len(b) to determine b
# use len(b) to determine f
def resolveOneJumpNested(source):
	source_string = ''
	if type(source) == list:
		source_string = ''.join(source)
	elif type(source) == str:
		source_string = source
		source = list(source)

	source_splitted = source_string.split('!', 4)
	if len(source_splitted) < 5:
		return source
	p_labelB_q, labelF_name, r, labelB_name, s_labelF_t = source_splitted

	p_labelB_q_splitted = p_labelB_q.rsplit(':' + labelB_name + ':', 1)
	if len(p_labelB_q_splitted) < 2:
		return source
	p, q = p_labelB_q_splitted

	s_labelF_t_splitted = s_labelF_t.rsplit(':' + labelF_name + ':', 1)
	if len(s_labelF_t_splitted) < 2:
		return source
	s, t = s_label_t_splitted

	len_q = get_source_length(q)
	len_r = get_source_length(r)
	len_s = get_source_length(s)
	if len_q is None or len_r is None or len_s is None:
		return source

	opF = '"+"+"+'
	opB = '"+"+"+'

	ans = p + ':' + labelB_name + ':' + q +\
			'0=' + opF + '^' +\
			r +\
			'0=' + opB + '^' +\
			s + ':' + labelF_name + ':' + t

	return list(ans)


# labels are no longer needed
def removeLabels(source):
	#print(source)
	return ''.join(re.split(':[^:]+:', ''.join(source)))

def resolveJump(source):
	before = source
	after = source
	while True:
		while True:
			before = after
			after = resolveOneJumpForward(before)
			if before == after:
				break
		while True:
			before = after
			after = resolveOneJumpBackward(before)
			if before == after:
				break

		# now there are no jump except _:B:_!A!_!B!_:A:_
		# special treatment needed
		after = resolveOneJumpNested(before)
		if before == after:
			break

	return removeLabels(after)

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

	# branch zero or non-zero
	source_string = '00="+"+"+""!A1!.00=.:A0:0=!A2!.0.:A2:'

	# single loop
	#source_string = '00="+""+"++:A1:00=-"."0=!A1!00="+""+"++:A2:00=-"."0=!A2!'

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

	hoge = resolveJump(source_string)
	print(hoge)
	#main.DEBUG_OUTPUT = True
	main.execute(hoge)
	exit(0)

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
