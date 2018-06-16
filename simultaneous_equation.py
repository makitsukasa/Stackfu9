# solve simultaneous equation for tag jump in sfw92sf9
#
# (ex)
# 	eval({0}) =            len({1}) + 10
# 	eval({1}) = len({0}) + len({1}) + 15
#
# solve([
# 	[False, True , 10],
# 	[True , True , 15],
# ])
#
# {0} = '""++"+"+"+',     eval({0}) = 24, len({0}) = 10
# {1} = '"""++"+"++""++', eval({1}) = 39, len({1}) = 14
#

import sys
from pick_number import pickNumber
from main import execPickedNumber

def solve_recur(equation, ans, row):
	if row < 0:
		return
	new_ans_evaluated = equation[row][-1]
	for i in range(len(equation[row]) - 1):
		if(equation[row][i]):
			new_ans_evaluated += len(ans[i])

	new_ans = pickNumber(new_ans_evaluated)
	if ans[row] != new_ans:
		if execPickedNumber(ans[row]) > execPickedNumber(new_ans):
			hoge = new_ans
			new_ans = ans[row]
			while len(new_ans) < len(hoge):
				new_ans += '0+'
			ans[row] = new_ans
			solve_recur(equation, ans, row - 1)
		else:
			ans[row] = new_ans
			solve_recur(equation, ans, len(equation) - 1)
	else:
		solve_recur(equation, ans, row - 1)

def solve(equation):
	rows = len(equation)
	ans = ['"-' for _ in range(len(equation))]
	solve_recur(equation, ans, rows - 1)
	return ans

if __name__ == '__main__':
	# example written at the beginning
	_equation = [
		[False, True , 10],
		[True , True , 15],
	]
	# test fill nop
	_equation = [
		[False, False,  0],
		[False, True , 19],
	]
	# bigger euation
	equation = [
		[False, True , False, False, 100],
		[True , True , False, True , 140],
		[False, True , False, True ,  10],
		[False, False, False, True , 100],
	]
	ans = solve(equation)
	print(ans)
	ans_evaluated = [execPickedNumber(ans[i]) for i in range(len(ans))]
	print(ans_evaluated)
	print([len(ans[i]) for i in range(len(ans))])

