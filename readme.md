# Stackfu9
boxy

twitter:@tsukasa_boxy


## Stackfu9 is

- pronounced "stack fuck"
  - 9 is "kyuu" or "ku" in Japanese
- inspired by brainfuck
- not derived from brainfuck
- not related to [Stackfuck](https://github.com/fxcqz/stackfuck)
  - sorry confusing

## Stackfu9
- has a stack
- has 9 operands
- is turing complete
  - I'll make it [ELVM](https://github.com/shinh/elvm) backend

## Operands
- 0 (zero  ) : push 0
- + (add   ) : pop 2, add, then push
- - (sub   ) : pop 2, sub, then push
- = (equal ) : pop 2, push 1(equal) or 0(not)
- " (dup   ) : duplicate stack top.
- ^ (jump  ) : pop 1, jump
- % (roll  ) : pop 1, roll
- . (output) : input a character and push
- , (input ) : pop 1, output the character

####jump
Pop stack top and let this be n.  
If n is positive, jump right n-th.  
If n is negative, jump left n-th.  
(I mean "Jump n-th", not "Jump to label".)

####roll
Pop stack top and let this be n.  
Pop the stack top and insert it at the n-th of stack.

    | a b c d e f g 4
    ↓roll
    | a b c g d e f
            ^ now g is 4th of stack
