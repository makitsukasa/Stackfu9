# Stackfu9Writable
Stackfu9Writable is a Stackfu9 extension.
It's sf9 with new sugar syntaxes.
- !LABEL_NAME! jumps to label if zero
- :LABEL_NAME: defines label
- [  jumps past the matching ']' if 0
- ]  jumps back to the matching '['
- <  evaluates to 1 if the stack top is less    than             zero, and otherwise to 0
- \> evaluates to 1 if the stack top is greater than             zero, and otherwise to 0
- {  evaluates to 1 if the stack top is less    than or equal to zero, and otherwise to 0
- }  evaluates to 1 if the stack top is greater than or equal to zero, and otherwise to 0
- @DECIMAL@ push immediate value
- CHARACTER push immediate value up to 126975 \u1efff

And some rules
- ignore nl '\n' and space ' '
- when label name is duplicated
	- forward jump has higher priority
		- ':A:p.!A!q.:A:r.' -> 'pr', not 'pppppp'...
	- shorter jump has higher priority
		- '!A!p.:A:q.:A:r.' -> 'qr', not 'r'
		- ':A:p.:A:q.!A!r.' -> 'qqqqqq'..., not 'pqpqpq'...

They are just sugar syntaxes. Use sf9w2sf9.py to desugar.
You can see sample at sf9w2sf9/sample.

## usage
```
python sf9w2sf9.py hoge.sf9w hoge.sf9
python sf9.py hoge.sf9
```
or
```
sh runsf9w.sh hoge.sf9w
```
