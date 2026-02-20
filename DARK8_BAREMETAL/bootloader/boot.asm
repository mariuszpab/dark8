[BITS 16]
[ORG 0x7C00]

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax

    mov si, msg16
    call print16

    ; A20
    in al, 0x92
    or al, 00000010b
    out 0x92, al

    ; GDT
    lgdt [gdt_descriptor]

    ; Protected Mode
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    jmp 0x08:pm_entry

print16:
    mov ah, 0x0E
.next:
    lodsb
    test al, al
    jz .done
    int 0x10
    jmp .next
.done:
    ret

msg16 db "DARK8 BOOTING...",0

; ---------------- GDT ----------------
gdt_start:
    dq 0
    dq 0x00CF9A000000FFFF
    dq 0x00CF92000000FFFF
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; ============================================================
; ======================= 32-BIT KERNEL =======================
; ============================================================

[BITS 32]
pm_entry:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov esp, 0x90000

    call kmain

.hang:
    jmp .hang

; ======== KERNEL (32-bit) ========

VIDEO_MEM   equ 0xB8000
SCREEN_W    equ 80
SCREEN_H    equ 25

cursor_pos  dd 0        ; aktualna pozycja kursora (0..(80*25-1))

kmain:
    call kclear_screen

    mov esi, msg1
    call kprintln

    mov esi, msg2
    call kprintln

    mov esi, msg3
    call kprintln

    ret

; ---------------- PRINT FUNCTIONS ----------------

kputc:
    ; AL = znak
    mov eax, [cursor_pos]

    cmp al, 10          ; '\n' ?
    je .newline

    mov edi, VIDEO_MEM
    add edi, eax
    shl edi, 1          ; *2 bo znak + kolor

    mov ah, 0x0F        ; biały
    mov [edi], ax

    inc eax
    mov [cursor_pos], eax
    jmp .done

.newline:
    mov ebx, SCREEN_W
    xor edx, edx
    div ebx
    inc eax
    mul ebx
    mov [cursor_pos], eax

.done:
    call kscroll
    ret

kputs:
.next:
    mov al, [esi]
    cmp al, 0
    je .done
    call kputc
    inc esi
    jmp .next
.done:
    ret

kprintln:
    call kputs
    mov al, 10
    call kputc
    ret

; ---------------- SCROLLING ----------------

kscroll:
    mov eax, [cursor_pos]
    cmp eax, SCREEN_W * SCREEN_H
    jb .done

    mov esi, VIDEO_MEM + SCREEN_W*2
    mov edi, VIDEO_MEM
    mov ecx, (SCREEN_H-1)*SCREEN_W
.copy:
    mov ax, [esi]
    mov [edi], ax
    add esi, 2
    add edi, 2
    loop .copy

    mov ecx, SCREEN_W
    mov ax, 0x0720
.clear:
    mov [edi], ax
    add edi, 2
    loop .clear

    mov eax, (SCREEN_H-1)*SCREEN_W
    mov [cursor_pos], eax

.done:
    ret

; ---------------- CLEAR SCREEN ----------------

kclear_screen:
    mov edi, VIDEO_MEM
    mov ecx, SCREEN_W * SCREEN_H
    mov ax, 0x0720
.fill:
    mov [edi], ax
    add edi, 2
    loop .fill

    mov dword [cursor_pos], 0
    ret

; ---------------- TEXTS ----------------

msg1 db "DARK8 KERNEL STARTED",0
msg2 db "VGA TEXT DRIVER ONLINE",0
msg3 db "SCROLL + NEWLINE READY",0

; ---------------- BOOT SIGNATURE ----------------

times 510-($-$$) db 0
dw 0xAA55
