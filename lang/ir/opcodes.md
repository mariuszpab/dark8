# DARK8 bytecode opcodes (initial proposal)

LOAD name   ; load variable
STORE name  ; store variable
PUSH value  ; push literal
POP         ; pop value
CALL name n ; call function with n args
RET         ; return
ADD|SUB|MUL|DIV ; arithmetic on stack
JUMP target
JUMP_IF target
NOP

; stack-based machine
