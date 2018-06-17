# '__M__[__N__]' => '__M__:B:"0=!F!__N__00=!B!:F:'
def solve(source, offset = 0):
	i = 0
	ans = ''
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
				ans_in_loop += solve(nested_part, i)
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
