[BITS 32]
[ORG 0x1000]

start:
    mov edi, 0xB8000
    mov esi, msg

.next:
    mov al, [esi]
    cmp al, 0
    je .done
    mov ah, 0x0F
    mov [edi], ax
    add edi, 2
    inc esi
    jmp .next

.done:
    jmp $

msg db "DARK8 KERNEL (MINIMAL 32-BIT)",0
