#include <stdint.h>

void isr_common_handler(uint32_t int_no, uint32_t err_code) {
    (void)int_no;
    (void)err_code;
    // Na razie nic – tylko po to, żeby linker był zadowolony
}

void irq_common_handler(uint32_t int_no, uint32_t err_code) {
    (void)int_no;
    (void)err_code;
    // Na razie nic – tylko po to, żeby linker był zadowolony
}

void kernel_main() {
    volatile char* vga = (volatile char*)0xB8000;
    vga[0] = 'K';
    vga[1] = 0x0F;   // biały na czarnym

    while (1) {
        __asm__ __volatile__("hlt");
    }
}

