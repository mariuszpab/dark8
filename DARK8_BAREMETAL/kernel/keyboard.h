#ifndef D8_KEYBOARD_H
#define D8_KEYBOARD_H

#include <stdint.h>

void keyboard_init();
void keyboard_on_scancode(uint8_t scancode);
void keyboard_irq_handler();

#endif

