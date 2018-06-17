# s    f 9w        2  s    f 9             .py
# Stackfu9Writable to Stackfu9 interpreter
#
# python sf9w2sf9.py input.sf9w output.sf9
#
# see sf9w.md

import sys
import sf9
sys.path.append('sf9w2sf9')
from immediate_value import solve as solveImmediateValue
from compare         import solve as solveCompare
from loop            import solve as solveLoop
from jump            import solve as solveJump

def solve(source):
	print_flag = False
	if print_flag: print(source)

	source = solveImmediateValue(source)
	if print_flag: print('immediate value')
	if print_flag: print(source)

	source = solveCompare(source)
	if print_flag: print('compare')
	if print_flag: print(source)

	source = solveLoop(source)
	if print_flag: print('loop')
	if print_flag: print(source)

	source = solveJump(source)
	if print_flag: print('jump')
	if print_flag: print(source)

	return source

if __name__ == '__main__':
	# print Hello World!
	_source = 'H.e.l.l.o. .w.o.r.l.d.\n.'

	# single loop
	_source = 'A[00=-".]^D[00="+"+-".]^'
	_source = '00="+""+"++[00=-".]^'

	# nested loop
	source = '00="+""+"++["[".00=-]^00=-]^'

	# positive or negative
	_source = '00="+"+"+"[00=-"0="""++""++"++"+"+^00=%00=+"0=""+"+"+"+"+"++^00=%]^0=^00="""+"++^^0=^0.'

	# 2<  2>  2{  2}  -1<  -1>  -1{  -1}  0<  0>  0{  0}
	_source = '00="+<.00="+>.00="+{.00="+}.00=""+-<.00=""+->.00=""+-{.00=""+-}.0<.0>.0{0+.0}.'
	_source = '0{.'

	# branch zero or non-zero
	_source = '00="+"+"+""!A1!.00=.:A1:0=!A2!.0.:A2:'

	# single loop
	_source = '00="+""+"++:A1:00=-"."0=!A1!00="+""+"++:A2:00=-"."0=!A2!'

	# nested jump
	_source = '00="+"+"+:2:"!1!00=-"."0=!2!:1:^0:4:"!3!00=-"."0=!4!:3:^'

	# nested nested jump
	_source = '00="+""+"++:O1:""!O2!:I1:"!I2!00=-"."0=!I1!:I2:^00=-"0=!O1!:O2:^'

	# fizzbuzz
	# it takes a few seconds to execute
	source = \
		'0x["00=-]^[000=%'\
			'"00=[0=^00=""++-">]^0=!ENDFIZZ!'\
			'F.i.z"..00=%00=+00=%:ENDFIZZ:'\
			'"00=[0=^00=""+"++-">]^0=!ENDBUZZ!'\
			'B.u.z"..00=%00=+00=%:ENDBUZZ:'\
			'00=%0=0="+^".0=^00="+""+"++.'\
		']^'

	if len(sys.argv) > 1:
		source = open(sys.argv[1]).read()

	source_sf9 = solve(source)

	if len(sys.argv) > 2:
		open(sys.argv[2], 'w').write(source_sf9)

	#sf9.DEBUG_OUTPUT = True
	#sf9.OUTPUT_AS_CHARACTER = True
	#sf9.execute(source_sf9)
