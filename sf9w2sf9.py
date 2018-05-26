# s    f 9w        2  s    f 9             .py
# Stackfu9Writable to Stackfu9 interpreter
#
# python sf9w2sf9.py input.sf9w output.sf9

# StackfuckWritable has
# - [         | jump past the matching ']' if 0
# - ]         | jump back to the matching '['
# - character | push immediate value

import linecache
import main

PICKNUMBER_OFFSET = 278
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
]

def opImmidiateValue(val, header = True, fill = None):
	if val == 0:
		return '0'

	elif val > 0:
		target_line = linecache.getline('pick_number.txt', val + PICKNUMBER_OFFSET)
		target = target_line.split(' ')[-1].strip()

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

def opImmidiateValueWithOverhead(val, overhead):
	target_line = linecache.getline('pick_number.txt', val + PICKNUMBER_OFFSET)
	target = target_line.split(' ')[-1].strip()
	return '00=' + target

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

def pickNumber(val):
	return val

def resolveJump(source):
	i = 0
	ans = []
	while i < len(source):

		if source[i] is ']':
			print("error : ']' detected without '['")
			return ""
		if source[i] is not '[':
			ans += source[i]
			i += 1
			continue

		ans_in_loop = ""
		i += 1
		while source[i] is not ']':
			ans_in_loop += source[i]
			if i >= len(source):
				print("error : ']' is not found after '['")
				return ""
			i += 1

		ans += '"0='
		num = len(ans_in_loop) + PICKNUMBER_OVERHEAD_WITH_HEADER
		ans += list(opImmidiateValue(num,
				header = False, fill = PICKNUMBER_OVERHEAD))
		ans += '^'
		ans += ans_in_loop
		num = -len(ans_in_loop) - PICKNUMBER_OVERHEAD_WITH_HEADER - PICKNUMBER_OVERHEAD - 5
		ans += list(opImmidiateValue(num,
				header = True, fill = PICKNUMBER_OVERHEAD))
		ans += '^'
		i += 1

	return ans

if __name__ == '__main__':
	# print Hello World!
	#source_string = 'H.e.l.l.o. .w.o.r.l.d.!.\n.'

	# goto test
	source_string = 'A[00=-".]^'

	source = list(source_string)
	source = resolveImmediateValue(source)
	source = resolveJump(source)

	#print(source)
	print(''.join(source))

	main.DEBUG_OUTPUT = False
	main.run(source)
