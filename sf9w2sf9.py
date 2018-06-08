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
		return '0'

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
		tagB_name = '📜B' + str(loop_start_pos)
		tagF_name = '📜F' + str(loop_start_pos)
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
	while True:
		while True:
			before = after
			after = resolveJumpOnceForward(before)
			if before == after:
				break
		while True:
			before = after
			after = resolveJumpOnceBackward(before)
			if before == after:
				break

		# now there are no jump except _:B:_!A!_!B!_:A:_
		# special treatment needed
		after = resolveJumpOnceNested(before)
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
	source_string = '00="+"+"+""!A1!.00=.:A1:0=!A2!.0.:A2:'

	# single loop
	source_string = '00="+""+"++:A1:00=-"."0=!A1!00="+""+"++:A2:00=-"."0=!A2!'

	# nested jump
	source_string = '00="+"+"+:1:"!2!00=-"."0=!1!:2:^0:3:"!4!00=-"."0=!3!:4:^'

	# nested nested jump
	source_string = '00="+""+"++:O1:""!O2!:I1:"!I2!00=-"."0=!I1!:I2:^00=-"0=!O1!:O2:^'

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

	print(source_string)
	source = list(source_string)
	source = resolveImmediateValue(source)
	source = resolveCompare(source)
	source = resolveLoop(source)
	print(''.join(source))
	source = resolveJump(source)

	#print(source)
	print(''.join(source))

	if len(sys.argv) > 2:
		open(sys.argv[2], 'w').write(''.join(source))

	#main.DEBUG_OUTPUT = True
	#main.OUTPUT_AS_CHARACTER = True
	main.execute(source)
