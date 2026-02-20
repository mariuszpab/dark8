#include <stdint.h>
#include "idt.h"
#include "pic.h"

volatile char* const VGA = (char*)0xB8000;

static void vga_puts(const char* s, int row, int col, uint8_t color) {
    int i = 0;
    int pos = (row * 80 + col) * 2;
    while (s[i]) {
        VGA[pos]     = s[i];
        VGA[pos + 1] = color;
        pos += 2;
        i++;
    }
}

void kmain(void) {
    vga_puts("DARK8 KERNEL C OK", 0, 0, 0x0F);

    idt_init();
    pic_remap();

    asm volatile("sti");

    for (;;) {
        asm volatile("hlt");
    }
}
