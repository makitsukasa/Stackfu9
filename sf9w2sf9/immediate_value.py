import lib
import pick_number

# bf9 does not follow immidiate value
# pickNumber() to get operand that push val onto stack top
def opImmidiateValue(val, header = True, fill = None):
	if val == 0:
		return '"-'

	elif val > 0:
		op = pick_number.pickNumber(val)

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
def solve(source):

	source_splitted = source.split('@')
	for i in range(1, len(source_splitted), 2):
		decimal = int(source_splitted[i])
		source_splitted[i] = '00=' + pick_number.pickNumber(decimal)
	source = ''.join(source_splitted)

	ans = ''
	for op in source:
		if op in lib.opListSF9 or op in lib.opListSF9W:
			ans += op
		else: # immidiate value
			ans += opImmidiateValue(ord(op))
	return ans
