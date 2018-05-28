import random
import main

# range to calculate accurately
RANGE = 20000

prime_memo = [None for i in range(RANGE + 1)]
ans_memo = [None for i in range(RANGE + 1)]

# Miller-Rabin
# https://qiita.com/srtk86/items/609737d50c9ef5f5dc59
def isPrime(n):
	if n == 2: return True
	if n == 1 or n & 1 == 0: return False

	if prime_memo[n] is not None:
		return prime_memo[n]

	d = (n - 1) >> 1
	while d & 1 == 0:
		d >>= 1

	for _ in range(100):
		a = random.randint(1, n - 1)
		t = d
		y = pow(a, t, n) # (a ** t) % n

		while t != n - 1 and y != 1 and y != n - 1:
			y = (y * y) % n
			t <<= 1

		if y != n - 1 and t & 1 == 0:
			if n < RANGE:
				prime_memo[n] = False;
			return False

	if n < RANGE:
		prime_memo[n] = True;
	return True

def recur(target, is_1_origin = True):

	ans = None;

	if target <= RANGE and ans_memo[target] is not None:
		return ans_memo[target]

	if target == 0:
		print("target is zero")
		ans = 'VERY_VERY_LONG_DUMMY_STRING'
		ans_memo[target] = ans
		return ans

	if target == 1:
		ans = ''
		ans_memo[target] = ans
		return ans

	if target % 2 == 0:
		ans2 = recur(target // 2) + '"+'
		if ans is None:
			ans = ans2
		else:
			ans = ans if (len(ans) <= len(ans2)) else ans2

	elif target % 3 == 0:
		ans2 = recur(target // 3) + '""++'
		if ans is None:
			ans = ans2
		else:
			ans = ans if (len(ans) <= len(ans2)) else ans2

	elif target % 5 == 0:
		ans2 = recur(target // 5) + '""+"++'
		if ans is None:
			ans = ans2
		else:
			ans = ans if (len(ans) <= len(ans2)) else ans2

	# skip heavy operation when target is large.
	if target <= RANGE:
		for p in range(7, target, 2):
			if not isPrime(p):
				continue
			if target > p and target % p == 0:
				ans2 = recur(p) + '"' +\
					recur(target // p - 1, False) + '+'
				if ans is None:
					ans = ans2
				else:
					ans = ans if (len(ans) <= len(ans2)) else ans2

	# ans is None => no idea => compromise
	# ans is 1_origin and odd => may be shorten by light operation
	if ans is None or is_1_origin and target % 2 == 1:
		ans2 = '"' + recur(target - 1) + '+'
		if ans is None:
			ans = ans2
		else:
			ans = ans if (len(ans) <= len(ans2)) else ans2

	if target <= RANGE:
		ans_memo[target] = ans

	return ans

def pickNumber(specific_number = None):
	begin = 1
	end = RANGE
	if specific_number is not None:
		begin = end = specific_number

	for i in range(begin, end + 1):
		ans = recur(i)
		if __name__ == '__main__':
			print(i, "is", len(ans), "chars", ans)

	return ans

if __name__ == '__main__':
	limit = 2 ** 31
	#main.DEBUG_OUTPUT = False
	for i in sorted(random.sample(range(limit // 2, limit), 1)):
		op = '00=' + pickNumber(i) + '.'
		main.execute(op)
