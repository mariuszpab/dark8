#include "keyboard.h"
#include "pic.h"
#include <stdint.h>

#define KBD_DATA_PORT 0x60

static inline uint8_t inb(uint16_t port) {
    uint8_t ret;
    __asm__ __volatile__("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}

static const char scancode_map[128] = {
    0,  27, '1','2','3','4','5','6','7','8','9','0','-','=', '\b',
    '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n', 0,
    'a','s','d','f','g','h','j','k','l',';','\'','`', 0, '\\',
    'z','x','c','v','b','n','m',',','.','/', 0, '*', 0, ' ',
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
};

void keyboard_init() {
    // nic nie trzeba robić
}

void keyboard_on_scancode(uint8_t scancode) {
    if (!(scancode & 0x80)) {
        char c = scancode_map[scancode];
        if (c) {
            volatile char* vga = (volatile char*)0xB8000;
            vga[2] = c;
            vga[3] = 0x0F;
        }
    }
}

void keyboard_irq_handler() {
    uint8_t sc = inb(KBD_DATA_PORT);
    keyboard_on_scancode(sc);
    pic_send_eoi(1);
}

