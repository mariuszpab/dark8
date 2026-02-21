[BITS 16]
[ORG 0x7C00]

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov si, msg_boot
    call print

    ; DAP dla LBA 1 (stage2)
    mov si, dap
    mov byte [si], 0x10       ; size
    mov byte [si+1], 0x00     ; reserved
    mov word [si+2], 1        ; sectors to read
    mov dword [si+4], 1       ; LBA = 1
    mov word [si+8], 0x7E00   ; offset
    mov word [si+10], 0x0000  ; segment

    mov ah, 0x42
    mov dl, 0x80              ; dysk twardy 0
    int 0x13
    jc disk_error

    jmp 0x0000:0x7E00

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

msg_boot db "BOOT...",0
msg_err  db "DISK ERR",0

dap:
    times 16 db 0

times 510-($-$$) db 0
dw 0xAA55

