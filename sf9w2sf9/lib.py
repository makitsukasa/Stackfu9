import re

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

opListSF9WCompare = [
	'<', # less than zero
	'>', # greater than zero
	'{', # less than or equal to zero
	'}', # greater than or equal to zero
]

opListSF9W = [
	'!', # jump to label if zero
	':', # define label
	'[', # loop like brainfuck
	']',
] + opListSF9WCompare

def get_source_length(source):
	if '!' in source:
		return None

	source_without_label_list = re.split(':[^:]+:', source)
	return len(''.join(source_without_label_list))

def get_source_length_without_label(source):
	return get_source_length(''.join(source.split('!')[0::2]))
