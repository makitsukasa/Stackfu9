import lib

def opCompare(op, index):
	zero_label     = '🏅{0}'.format(index)
	one_label      = '🥇{0}'.format(index)
	push_one_label = '🥈{0}'.format(index)
	end_label      = '🥉{0}'.format(index)
	labels = [zero_label, one_label, push_one_label, end_label]

	IS_ZERO_SKIP_ALL  = '"!{0[3]}!'.format(labels)
	IS_ZERO_JUMP_TO_1 = '"!{0[2]}!'.format(labels)
	IS_POS = '"[00=-"!{0[1]}!00=%00=+"!{0[0]}!00=%]'\
			':{0[1]}:^"-^0:{0[2]}:0=0!{0[3]}!:{0[0]}:^"-:{0[3]}:'
	IS_NEG = '"[00=+"!{0[1]}!00=%00=-"!{0[0]}!00=%]'\
			':{0[1]}:^"-^0:{0[2]}:0=0!{0[3]}!:{0[0]}:^"-:{0[3]}:'
	IS_POS = IS_POS.format(labels)
	IS_NEG = IS_NEG.format(labels)

	if op is '<': # less than zero
		return IS_ZERO_SKIP_ALL + IS_NEG
	if op is '>': # greater than zero
		return IS_ZERO_SKIP_ALL + IS_POS
	if op is '{': # less than or equal to zero
		return IS_ZERO_JUMP_TO_1 + IS_NEG
	if op is '}': # greater than or equal to zero
		return IS_ZERO_JUMP_TO_1 + IS_POS

# @param source that not resolved compares
# @return source that resolved compares
def solve(source):
	ans = ''
	index = 0
	for op in source:
		if op in lib.opListSF9WCompare:
			ans += opCompare(op, index)
			index += 1
		else:
			ans += op
	return ans
