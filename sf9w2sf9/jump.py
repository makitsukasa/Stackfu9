import re
import jump_simequ
import lib

def makeSimEqu_recur(source_string, index, equation):
	source_string_replaced = source_string.replace('!', '📍', index * 2)
	source_splitted = source_string_replaced.split('!', 2)
	if len(source_splitted) < 3:
		#print("end")
		return
	backward, label_name, forward = source_splitted
	backward      = backward.replace('📍', '!')
	forward       = forward .replace('📍', '!')
	backward_splitted = backward.split(':' + label_name + ':', 1)
	forward_splitted  = forward .split(':' + label_name + ':', 1)

	if len(backward_splitted) == 2:
		#print(label_name, "backward")
		op_in_jump = backward_splitted[1]
		jump_in_jump_count = len(op_in_jump.split('!')) // 2
		for i in range(index, index - jump_in_jump_count - 1, -1):
			equation[index][i] = True
		equation[index][-1] = lib.get_source_length_without_label(op_in_jump)
		#print(equation[index])

	elif len(forward_splitted) == 2:
		#print(label_name, "forward")
		op_in_jump = forward_splitted[0]
		jump_in_jump_count = len(op_in_jump.split('!')) // 2
		for i in range(index + 1, index + jump_in_jump_count + 1):
			equation[index][i] = True
		equation[index][-1] = lib.get_source_length_without_label(op_in_jump)
		#print(equation[index])

	else:
		print("error : label not found")
		return

	makeSimEqu_recur(source_string, index + 1, equation)

# labels are no longer needed
def removeLabels(source):
	#print(source)
	return ''.join(re.split(':[^:]+:', ''.join(source)))

def solve(source):
	source_splitted = source.split('!')
	opJumpNum = len(source_splitted) // 2
	if opJumpNum != 0:
		equation = [[False for _ in range(opJumpNum)] for _ in range(opJumpNum)]
		for i in range(len(equation)):
			equation[i].append(0)
		makeSimEqu_recur(source, 0, equation)
		operands = jump_simequ.solve(equation)
		#print([main.execPickedNumber(op) for op in operands])
		ans = ''
		for i in range(len(source_splitted)):
			if i % 2 == 0:
				ans += source_splitted[i]
			else:
				ans += '0=' + operands[i // 2] + '^'

	return removeLabels(ans)
