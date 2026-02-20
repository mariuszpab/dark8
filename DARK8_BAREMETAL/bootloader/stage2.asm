[BITS 16]
[ORG 0x7E00]

start:
    mov si, msg2
    call print

    ; przygotuj DAP dla LBA
    mov si, dap
    mov ah, 0x42
    mov dl, 0          ; A:
    int 0x13
    jc disk_error

    mov si, msg_loaded
    call print

    ; A20
    in al, 0x92
    or al, 00000010b
    out 0x92, al

    ; GDT
    lgdt [gdt_descriptor]

    ; PM
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    jmp 0x08:pm_entry

disk_error:
    mov si, msg_err
    call print
    jmp $

print:
    mov ah, 0x0E
.next:
    lodsb
    test al, al
    jz .done
    int 0x10
    jmp .next
.done:
    ret

msg2       db "STAGE2 LBA",0
msg_loaded db " KERNEL LOADED",0
msg_err    db " LBA ERR",0

; DAP – czytamy np. 8 sektorów od LBA 2 do 0x1000
dap:
    db 16           ; rozmiar
    db 0
    dw 8            ; liczba sektorów
    dw 0x1000       ; offset
    dw 0x0000       ; segment
    dq 2            ; LBA start (sektor 2)

; GDT
gdt_start:
    dq 0x0000000000000000
    dq 0x00CF9A000000FFFF ; code
    dq 0x00CF92000000FFFF ; data
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

[BITS 32]
pm_entry:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov esp, 0x90000

    jmp 0x1000       ; skok do kernela

times 512-($-$$) db 0
