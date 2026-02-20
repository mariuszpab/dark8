#include <stdint.h>
#include "pic.h"

static volatile char* const VGA = (char*)0xB8000;
static int cursor = 0;

static inline uint8_t inb(uint16_t port) {
    uint8_t val;
    asm volatile("inb %1, %0" : "=a"(val) : "Nd"(port));
    return val;
}

static char scancode_to_char(uint8_t sc) {
    static const char map[128] = {
        0,  27, '1','2','3','4','5','6','7','8','9','0','-','=', '\b',
        '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n', 0,
        'a','s','d','f','g','h','j','k','l',';','\'','`', 0,'\\',
        'z','x','c','v','b','n','m',',','.','/', 0,   0,   0,   ' '
    };
    if (sc < 128) return map[sc];
    return 0;
}

void keyboard_isr_c(void) {
    uint8_t sc = inb(0x60);
    char c = scancode_to_char(sc);

    if (c) {
        VGA[cursor * 2]     = c;
        VGA[cursor * 2 + 1] = 0x0F;
        cursor++;
    }

    pic_send_eoi();
}
