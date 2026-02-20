#include "idt.h"
#include "keyboard.h"

#define IDT_SIZE 256

static struct idt_entry idt[IDT_SIZE];
static struct idt_ptr   idtp;

static void idt_set_gate(int n, uint32_t handler, uint16_t sel, uint8_t flags) {
    idt[n].offset_low  = handler & 0xFFFF;
    idt[n].selector    = sel;
    idt[n].zero        = 0;
    idt[n].type_attr   = flags;
    idt[n].offset_high = (handler >> 16) & 0xFFFF;
}

void isr_keyboard_stub(void) {
    asm volatile("pusha");
    keyboard_isr_c();
    asm volatile("popa; iret");
}

void idt_init(void) {
    idtp.limit = sizeof(idt) - 1;
    idtp.base  = (uint32_t)&idt;

    for (int i = 0; i < IDT_SIZE; i++) {
        idt[i].offset_low  = 0;
        idt[i].selector    = 0;
        idt[i].zero        = 0;
        idt[i].type_attr   = 0;
        idt[i].offset_high = 0;
    }

    idt_set_gate(0x21, (uint32_t)isr_keyboard_stub, 0x08, 0x8E);

    asm volatile("lidt (%0)" :: "r" (&idtp));
}
