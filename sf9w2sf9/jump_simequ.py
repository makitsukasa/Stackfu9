# solve simultaneous equation for tag jump in sfw92sf9
#
# (ex)
# 	eval({0}) =            len({1}) + 10
# 	eval({1}) = len({0}) + len({1}) + 10
#
# equation = [
# 	[False, True , 10],
# 	[True , True , 10],
# ]
# solve(equation)
#
# {0} = '""+"+"+"+"++0+',       eval({0}) = 33,  len({0}) = 14
# {1} = '"""+"+"+"++""++-0+0+', eval({1}) = -50, len({1}) = 20
#

from sys import getrecursionlimit, setrecursionlimit, path
from random import random, randrange
import pick_number
from sf9 import execPickedNumber

# @param equation [[False, True , 10], [True , True , 15],]
# @param ans ['"-', '"-'] when called,
#            ['""+"+"+"+"++0+', '"""+"+"+"++""++-0+0+'] when returns True
# @return succeed(True) or failue(False)
def solve_recur(equation, ans, row):
	# succeed all rows
	# return succeed
	if row >= len(equation):
		return True
	# if row == 0:
	# 	print('start', [execPickedNumber(ans[i]) for i in range(len(ans))], ans)

	new_ans_evaluated = equation[row][-1]
	for i in range(len(equation[row]) - 1):
		if(equation[row][i]):
			# += len('0=') + len(ans[i]) + len('^')
			new_ans_evaluated += len(ans[i]) + 3

	# jump forwawd or jump backward
	if equation[row][row]:
		new_ans_evaluated *= -1
		new_ans = '"' + pick_number.pickNumber(-new_ans_evaluated + 1) + '-'
	else:
		new_ans = pick_number.pickNumber(new_ans_evaluated)

	old_ans_evaluated = execPickedNumber(ans[row])
	# print(old_ans_evaluated, new_ans_evaluated)
	if old_ans_evaluated != new_ans_evaluated:
		if abs(old_ans_evaluated) > abs(new_ans_evaluated):
			if len(ans[row]) > len(new_ans):
				ans[row] = new_ans
				# print(row, "failue(C)", old_ans_evaluated, new_ans_evaluated)
				return False
			# reject new_ans
			# not to be shorter than prev, fill with nop '0+'
			if len(ans[row]) < len(new_ans):
				while len(ans[row]) < len(new_ans):
					ans[row] += '0+'
				# if backward jump, redo from the beginning
				if equation[row][row]:
					# print(row, "failue(B)", old_ans_evaluated, new_ans_evaluated)
					return False
			# do next row
			return solve_recur(equation, ans, row + 1)
		else:
			# not to be shorter than prev, fill with nop '0+'
			while len(ans[row]) > len(new_ans):
				new_ans += '0+'
			ans[row] = new_ans
			# Redo from the beginning
			# return failue
			#print(row, "failue(A)", old_ans_evaluated, new_ans_evaluated)
			return False
	else:
		# do next row
		return solve_recur(equation, ans, row + 1)

# @param equation [[False, True , 10],[True , True , 10],]
# @return ['""+"+"+"+"++0+', '"""+"+"+"++""++-0+0+']
def solve(equation):
	# for e in equation:
	# 	print(e)
	if len(equation) > getrecursionlimit():
		setrecursionlimit(len(equation) + 100)
	ans = ['"-' for _ in range(len(equation))]
	while not solve_recur(equation, ans, 0):
		pass
	# print([execPickedNumber(ans[i]) for i in range(len(ans))])
	return ans

def getRandomEquation(dim, randmax):
	eq = [[random() < 0.5 for _ in range(dim)] for _ in range(dim)]
	for i in range(dim):
		eq[i].append(randrange(randmax))
	return eq

if __name__ == '__main__':

	equationList = []
	_equationList = []

	# example written at the beginning
	# ans is [33, -50]
	_equationList.append([
		[False, True , 10],
		[True , True , 10],
	])
	# ans is [43, -62]
	_equationList.append([
		[False, True , 20],
		[True , True , 20],
	])
	_equationList.append([
		[False, True , 100],
		[True , True , 145],
	])
	# test fill nop
	# ans is [0, -38]
	_equationList.append([
		[False, False,  0],
		[False, True , 19],
	])
	# bigger equation
	_equationList.append([
		[False, True , False, False, 100],
		[True , True , False, True , 140],
		[False, True , False, True ,  10],
		[False, False, False, True , 100],
	])
	# equation in random state
	# A Much bigger equation takes about dim^2 * 10 miliseconds.
	equationList.append(getRandomEquation(50, randrange(100000)))

	for equation in equationList:
		print('[')
		for i in range(len(equation)):
			print('\t', equation[i], ',', sep = '')
		print(']')
		ans = solve(equation)
		print('ans :', ans)
		ans_evaluated = [execPickedNumber(ans[i]) for i in range(len(ans))]
		print('eval:', ans_evaluated)
		print('len :', [len(ans[i]) for i in range(len(ans))])
		# if equation == [[False, True , 10], [True , True , 10],] and ans_evaluated != [33, -50] or\
		#   equation == [[False, True , 20], [True , True , 20],] and ans_evaluated != [43, -62]:
		# 	print("INVALID")
		# 	exit(0)
