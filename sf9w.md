# Stackfu9Writable
Stackfu9Writable is a Stackfu9 extension.
It's sf9 with new sugar syntaxes.
- !LABEL_NAME! jumps to label if zero
- :LABEL_NAME: defines label
- [ jumps past the matching ']' if 0
- ] jumps back to the matching '['
- < evaluates to 1 if the stack top is less    than             zero, and otherwise to 0
- \> evaluates to 1 if the stack top is greater than             zero, and otherwise to 0
- { evaluates to 1 if the stack top is less    than or equal to zero, and otherwise to 0
- } evaluates to 1 if the stack top is greater than or equal to zero, and otherwise to 0
- character push immediate value up to 126975 \u1efff

They are just sugar syntaxes. Convert to sf9 with sf9w2sf9.py.
You can see sample at sf9w2sf9/sample.

## usage
```
python sf9w2sf9.py hoge.sf9w hoge.sf9
python sf9.py hoge.sf9
```
or
`sh runsf9w.sh hoge.sf9w`
