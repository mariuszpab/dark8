global kmain
extern kernel_main

section .text

kmain:
    call kernel_main
.hang:
    hlt
    jmp .hang

