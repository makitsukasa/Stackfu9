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
# - 'character' push immediate value up to 126975 \u1efff

import linecache
import sys
import re
import main
from pick_number import pickNumber
from simultaneous_equation import solve as solveSimEqu

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
		return '"-'

	elif val > 0:
		op = pickNumber(val)

		if fill is not None:
			while len(op) < fill:
				op += '0+'

		if header:
			op = '00=' + op

		return op

	else:
		fill = None if fill is None else fill - 2
		op = '"' + opImmidiateValue(-val + 1, header = False, fill = fill) + '-'

		if header:
			op = '00=' + op

		return op

# @param source that not resolved immidiate values
# @return source that resolved immidiate values
def resolveImmediateValue(source):
	ans = []
	for op in source:
		if op in opListSF9 or op in opListSF9W:
			ans += op
		else: # immidiate value
			ans += opImmidiateValue(ord(op))
	return ans

def get_source_length(source):
	if '!' in source:
		return None

	source_without_label_list = re.split(':[^:]+:', source)
	return len(''.join(source_without_label_list))

def get_source_length_without_label(source):
	return get_source_length(''.join(source.split('!')[0::2]))

def opCompare(op, index):
	IS_ZERO_SKIP_ALL  = '"0="""""+"++"+"+"++"++"++^'
	IS_ZERO_JUMP_TO_1 = '"0=""+"++""+"++""++"+0+0+^'
	IS_POS = '"[00=-"0="""++""++"++"+"+^00=%00=+"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0'
	IS_NEG = '"[00=+"0="""++""++"++"+"+^00=%00=-"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0'

	zero_label = '🏅{0}'.format(index)
	one_label  = '🥇{0}'.format(index)
	end_label  = '🥈{0}'.format(index)
	labels     = [zero_label, one_label, end_label]

	IS_ZERO_SKIP_ALL  = '"!{0[2]}!'.format(labels)
	IS_ZERO_JUMP_TO_1 = '"!{0[1]}!'.format(labels)
	IS_POS = '"[00=-"!{0[1]}!00=%00=+!{0[0]}!00=%]:{0[0]}:^00=0!{0[2]}!:{0[1]}:0:{0[2]}:'.format(labels)
	IS_NEG = '"[00=+"!{0[1]}!00=%00=-!{0[0]}!00=%]:{0[0]}:^00=0!{0[2]}!:{0[1]}:0:{0[2]}:'.format(labels)

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
	index = 0
	for op in source:
		if op in opListSF9WCompare:
			ans += opCompare(op, index)
			index += 1
		else:
			ans += op
	return ans

# '__M__[__N__]' => '__M__:B:"0=!F!__N__00=!B!:F:'
def resolveLoop(source, offset = 0):
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
		loop_start_pos = i + offset
		i += 1		# ignore '[' once
		while source[i] is not ']':
			if source[i] is '[':
				# loop is nested
				nested_part = []
				nest_depth = 0
				#print("nest from", i)
				while True:
					if source[i] is '[':
						#print(i, "is '['")
						nest_depth += 1
					elif source[i] is ']':
						#print(i, "is ']'")
						nest_depth -= 1
					nested_part += source[i]
					if nest_depth <= 0:
						break
					i += 1

				# now nested_part is like '[00000000]'
				#print("nested parts is", ''.join(nested_part))
				ans_in_loop += resolveLoop(nested_part, i)
			else:
				ans_in_loop += source[i]

			i += 1

			if i >= len(source):
				print("error : ']' is not found after '['", loop_start_pos)
				return ""

		# '__M__[__N__]' => '__M__:B:"0=!F!__N__00=!B!:F:'
		tagB_name = 'B📜' + str(loop_start_pos)
		tagF_name = 'F📜' + str(loop_start_pos)
		ans += ':' + tagB_name + ':' +\
		       '"' +\
		       '!' + tagF_name + '!' +\
		       ''.join(ans_in_loop) +\
		       '0!' + tagB_name + '!' +\
		       ':' + tagF_name + ':'

		i += 1

	return ans

# __p__!F!__q__:F:__r__ => __p__0=f^__q__:F:__r__
# easiest
def resolveJumpOnceForward(source, index = 0):
	source_string = ''.join(source)

	source_string = source_string.replace('!', '📍', index * 2)
	source_splitted = source_string.split('!', 2)
	if len(source_splitted) < 3:
		return source
	p, label_name, q_label_r = source_splitted
	source_string = source_string.replace('📍', '!')
	p = p.replace('📍', '!')

	q_label_r_splitted = q_label_r.split(':' + label_name + ':', 1)
	if len(q_label_r_splitted) < 2:
		return resolveJumpOnceForward(source, index + 1)
	q, r = q_label_r_splitted

	len_q = get_source_length(q)
	if len_q is None:
		return resolveJumpOnceForward(source, index + 1)

	ans = p + '0=' + opImmidiateValue(len_q, header = False) + '^' +\
			q + ':' + label_name + ':' + r

	return list(ans)

# __p__:B:__q__!B!__r__ => __p__:B:__q__b^__r__
# @param val is len(q)
# @return b
def opImmidiateValueBackward(val):
	b = val
	op_b = opImmidiateValue(-val, header = False)
	len_b = len(op_b)
	while b < len_b + val:
		b += 2
		op_b = opImmidiateValue(-b, header = False)
		len_b = len(op_b)

	op_b = opImmidiateValue(-b, header = False, fill = b - val)
	#print(b)
	return op_b

# __p__:B:__q__!B!__r__ => __p__:B:__q__0=b^__r__
# use len(b) to determine b
def resolveJumpOnceBackward(source, index = 0):
	source_string = ''.join(source)

	source_string = source_string.replace('!', '📍', index * 2)
	source_splitted = source_string.split('!', 2)
	if len(source_splitted) < 3:
		return source
	p_label_q, label_name, r = source_splitted
	source_string = source_string.replace('📍', '!')
	p_label_q = p_label_q.replace('📍', '!')
	r = r.replace('📍', '!')

	p_label_q_splitted = p_label_q.rsplit(':' + label_name + ':', 1)
	if len(p_label_q_splitted) < 2:
		return resolveJumpOnceBackward(source, index + 1)
	p, q = p_label_q_splitted

	len_q = get_source_length(q)
	if len_q is None:
		return resolveJumpOnceBackward(source, index + 1)

	ans = p + ':' + label_name + ':' + q +\
			'0=' + opImmidiateValueBackward(len_q + 3) + '^' + r

	return list(ans)

# __p__:B:__q__!F!__r__!B!__s__:F:__t__ => __p__:B:__q__0=f^__r__0=b^__s__:F:__t__
# @param overhead_f is len(r+s)+3
# @param overhead_b is len(q+r)+6
# @return b
def opImmidiateValueNested(overhead_f, overhead_b):
	op_f = ''
	op_b = ''
	b = 0
	len_f = 0
	len_b = overhead_b - 2

	while b < len_b + len_f + overhead_b:
		b += 2
		op_f = opImmidiateValue(overhead_f + len_b, header = False)
		len_f = len(op_f)
		op_b = opImmidiateValue(-b, header = False)
		len_b = len(op_b)

	#print(b, (len_b + len_f + overhead_b))
	op_b = opImmidiateValue(-b, header = False, fill = b - (len_f + overhead_b))

	#print("f is", overhead_f + len_b, ", b is", b)
	return op_f, op_b

# __p__:B:__q__!F!__r__!B!__s__:F:__t__ => __p__:B:__q__0=f^__r__0=b^__s__:F:__t__
# use len(f) + len(b) to determine b
# use len(b) to determine f
def resolveJumpOnceNested(source, index = 0):
	source_string = ''.join(source)

	source_string = source_string.replace('!', '📍', index * 2)
	source_splitted = source_string.split('!', 4)
	if len(source_splitted) < 5:
		return source
	p_labelB_q, labelF_name, r, labelB_name, s_labelF_t = source_splitted
	source_string = source_string.replace('📍', '!')
	p_labelB_q = p_labelB_q.replace('📍', '!')
	r = r.replace('📍', '!')

	p_labelB_q_splitted = p_labelB_q.rsplit(':' + labelB_name + ':', 1)
	if len(p_labelB_q_splitted) < 2:
		return resolveJumpOnceNested(source, index + 1)
	p, q = p_labelB_q_splitted

	s_labelF_t_splitted = s_labelF_t.split(':' + labelF_name + ':', 1)
	if len(s_labelF_t_splitted) < 2:
		return resolveJumpOnceNested(source, index + 1)
	s, t = s_labelF_t_splitted

	len_q = get_source_length(q)
	len_r = get_source_length(r)
	len_s = get_source_length(s)
	if len_q is None or len_r is None or len_s is None:
		return resolveJumpOnceNested(source, index + 1)

	op_f, op_b = opImmidiateValueNested(len_r + len_s + 3, len_q + len_r + 6)

	ans = p + ':' + labelB_name + ':' + q +\
	      '0=' + op_f + '^' + r +\
	      '0=' + op_b + '^' +\
	      s + ':' + labelF_name + ':' + t

	return list(ans)

# labels are no longer needed
def removeLabels(source):
	#print(source)
	return ''.join(re.split(':[^:]+:', ''.join(source)))

def resolveJump(source):
	before = source
	after = source
	changed = True
	while changed:
		while True:
			before = after
			#print('F')
			after = resolveJumpOnceForward(before)
			if before == after:
				break
			else:
				changed = True

		while True:
			before = after
			#print('B')
			after = resolveJumpOnceBackward(before)
			if before == after:
				break
			else:
				changed = True

		# now there are no jump except _:B:_!A!_!B!_:A:_
		# special treatment needed
		#print('N')
		after = resolveJumpOnceNested(before)
		if before == after:
			break
		else:
			changed = True

	return removeLabels(after)
	return after

def makeSimEqu_recur(source_string, index, equation):
	source_string_replaced = source_string.replace('!', '📍', index * 2)
	source_splitted = source_string_replaced.split('!', 2)
	if len(source_splitted) < 3:
		#print("end")
		return
	backward, label_name, forward = source_splitted
	backward      = backward     .replace('📍', '!')
	forward       = forward      .replace('📍', '!')
	backward_splitted = backward.split(':' + label_name + ':', 1)
	forward_splitted  = forward .split(':' + label_name + ':', 1)

	if len(backward_splitted) == 2:
		#print(label_name, "backward")
		op_in_jump = backward_splitted[1]
		jump_in_jump_count = len(op_in_jump.split('!')) // 2
		for i in range(index, index - jump_in_jump_count - 1, -1):
			equation[index][i] = True
		equation[index][-1] = get_source_length_without_label(op_in_jump)
		#print(equation[index])

	elif len(forward_splitted) == 2:
		#print(label_name, "forward")
		op_in_jump = forward_splitted[0]
		jump_in_jump_count = len(op_in_jump.split('!')) // 2
		for i in range(index + 1, index + jump_in_jump_count + 1):
			equation[index][i] = True
		equation[index][-1] = get_source_length_without_label(op_in_jump)
		#print(equation[index])

	else:
		print("error : label not found")
		return

	makeSimEqu_recur(source_string, index + 1, equation)

def resolveJump_SimEqu(source):
	source_string = ''.join(source)
	source_string_splitted = source_string.split('!')
	opJumpNum = len(source_string_splitted) // 2
	if opJumpNum != 0:
		equation = [[False for _ in range(opJumpNum)] for _ in range(opJumpNum)]
		for i in range(len(equation)):
			equation[i].append(0)
		makeSimEqu_recur(source_string, 0, equation)
		operands = solveSimEqu(equation)
		#print([main.execPickedNumber(op) for op in operands])
		ans = ''
		for i in range(len(source_string_splitted)):
			if i % 2 == 0:
				ans += source_string_splitted[i]
			else:
				ans += '0=' + operands[i // 2] + '^'

	return list(removeLabels(ans))

if __name__ == '__main__':
	# print Hello World!
	source_string = 'H.e.l.l.o. .w.o.r.l.d.!.\n.'

	# single loop
	_source_string = 'A[00=-".]^D[00="+"+-".]^'
	_source_string = '00="+""+"++[00=-".]^'

	# nested loop
	source_string = '00="+""+"++["[".00=-]^00=-]^'

	# positive or negative
	_source_string = '00="+"+"+"[00=-"0="""++""++"++"+"+^00=%00=+"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0.'

	# 2<  2>  2{  2}  -1<  -1>  -1{  -1}  0<  0>  0{  0}
	_source_string = '00="+<.00="+>.00="+{.00="+}.00=""+-<.00=""+->.00=""+-{.00=""+-}.0<.0>.0{0+.0}.'
	_source_string = '00=<.'

	# branch zero or non-zero
	_source_string = '00="+"+"+""!A1!.00=.:A1:0=!A2!.0.:A2:'

	# single loop
	_source_string = '00="+""+"++:A1:00=-"."0=!A1!00="+""+"++:A2:00=-"."0=!A2!'

	# nested jump
	_source_string = '00="+"+"+:2:"!1!00=-"."0=!2!:1:^0:4:"!3!00=-"."0=!4!:3:^'

	# nested nested jump
	_source_string = '00="+""+"++:O1:""!O2!:I1:"!I2!00=-"."0=!I1!:I2:^00=-"0=!O1!:O2:^'

	# fizzbuzz
	_source_string = \
		'000=""+"++""++"+"+["00=-]^[000=%'\
			'"00=[0=^00=""++-">]^0=0="""++"+"++""++"+^'\
			'00="""++"++""+"++"+.00="""++"++""+"++""++.00="""+"++""++"+"++"+"..00=%00=+00=%'\
			'"00=[0=^00=""+"++-">]^0=0="""++""++"++"+"+^'\
			'00=""+"+"+"+"++"+.00="""++"+"++""++""++.00="""+"++""++"+"++"+"..00=%00=+00=%'\
			'00=%0=0="+^".0=^00="+""+"++.'\
		']^'

	if len(sys.argv) > 1:
		source_string = open(sys.argv[1]).read()

	print(source_string)
	source = list(source_string)
	source = resolveImmediateValue(source)
	source = resolveCompare(source)
	print('compare')
	print(''.join(source))
	source = resolveLoop(source)
	print('loop')
	print(''.join(source))
	source = resolveJump_SimEqu(source)
	print('jump')
	print(''.join(source))

	if len(sys.argv) > 2:
		open(sys.argv[2], 'w').write(''.join(source))

	#main.DEBUG_OUTPUT = True
	#main.OUTPUT_AS_CHARACTER = True
	main.execute(source)
