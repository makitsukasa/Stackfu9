# Stackfu9
Stackfu9 interpreter in python.

## Stackfu9 is
- esolang I invented
- one-stack-oriented
- unlimited stack size, bignum cells
- 9 operands
- turing complete
  - I'll make it [ELVM](https://github.com/shinh/elvm) backend
- inspired by brainfuck
- not derived from brainfuck
- pronounced as "stack fuck"
  - 9 is "kyuu" or "ku" in Japanese
- not related to [Stackfuck](https://github.com/fxcqz/stackfuck)
  - sorry for confusing

## Operands
- 0  (zero)   : push 0
- \+ (add)    : pop 2 elements, add, then push
- \- (sub)    : pop 2 elements, sub, then push
- =  (equal)  : pop 2 elements, push 1(equal) or 0(not)
- "  (dup)    : duplicate stack top.
- ^  (jump)   : pop 1 element, jump
- %  (roll)   : pop 1 element, roll
- .  (output) : pop 1 element, output the character
- ,  (input)  : input a character and push

**jump**  
Pop the stack top and let this be n.  
If n is positive, jump right n-th.  
If n is negative, jump left n-th.  
(I mean "Jump n-th", not "Jump to label".)

**roll**  
Pop the stack top and let this be n.  
Pop the stack top and insert it at the n-th of the stack.

    | a b c d e f g 4
    ↓roll
    | a b g c d e f
          ^ now g is (4 + 1)th of stack
