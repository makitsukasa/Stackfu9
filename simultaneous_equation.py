# solve simultaneous equation for tag jump in sfw92sf9
#
# (ex)
# 	eval({0}) =            len({1}) + 10
# 	eval({1}) = len({0}) + len({1}) + 15
#
# equation = [
# 	[False, True , 10],
# 	[True , True , 15],
# ]
# solve(equation)
#
# {0} = '""++"+"+"+',     eval({0}) = 24, len({0}) = 10
# {1} = '"""++"+"++""++', eval({1}) = 39, len({1}) = 14
#

from sys import getrecursionlimit, setrecursionlimit
from random import random, randrange
from pick_number import pickNumber
from main import execPickedNumber

# @param equation [[False, True , 10],[True , True , 15],]
# @param ans ['"-', '"-'] when called,
#            ['""++"+"+"+', '"""++"+"++""++'] when returns True
# @return succeed(True) or failue(False)
def solve_recur(equation, ans, row):
	# succeed all rows
	# return succeed
	if row >= len(equation):
		return True

	new_ans_evaluated = equation[row][-1]
	for i in range(len(equation[row]) - 1):
		if(equation[row][i]):
			new_ans_evaluated += len(ans[i])

	new_ans = pickNumber(new_ans_evaluated)
	if ans[row] != new_ans:
		if execPickedNumber(ans[row]) > new_ans_evaluated:
			# reject new_ans
			# fill with nop '0+'
			while len(ans[row]) < len(new_ans):
				ans[row] += '0+'
			# do next row
			return solve_recur(equation, ans, row + 1)
		else:
			ans[row] = new_ans
			# Redo from the beginning
			# return failue
			return False
	else:
		# do next row
		return solve_recur(equation, ans, row + 1)

# @param equation [[False, True , 10],[True , True , 15],]
# @return ['""++"+"+"+', '"""++"+"++""++']
def solve(equation):
	if len(equation) > getrecursionlimit():
		setrecursionlimit(len(equation) + 100)
	ans = ['"-' for _ in range(len(equation))]
	while not solve_recur(equation, ans, 0):
		pass
	return ans

def getRandomEquation(dim, randmax):
	ans = [[random() < 0.5 for _ in range(dim)] for _ in range(dim)]
	for i in range(dim):
		ans[i].append(randrange(randmax))
	return ans

if __name__ == '__main__':

	# example written at the beginning
	equation = [
		[False, True , 10],
		[True , True , 15],
	]
	# test fill nop
	_equation = [
		[False, False,  0],
		[False, True , 19],
	]
	# bigger equation
	equation = [
		[False, True , False, False, 100],
		[True , True , False, True , 140],
		[False, True , False, True ,  10],
		[False, False, False, True , 100],
	]
	# much bigger equation in random state
	# It takes a few seconds.
	_equation = getRandomEquation(50, randrange(10000))

	print('[')
	for i in range(len(equation)):
		print('\t', equation[i], ',', sep = '')
	print(']')

	ans = solve(equation)
	print('ans :', ans)
	print('eval:', [execPickedNumber(ans[i]) for i in range(len(ans))])
	print('len :', [len(ans[i]) for i in range(len(ans))])
