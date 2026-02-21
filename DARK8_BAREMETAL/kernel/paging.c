#include "paging.h"
#include <stdint.h>

static page_directory_t* kernel_directory;
static page_table_t*     kernel_table;

static inline void load_page_directory(uint32_t addr) {
    __asm__ __volatile__("mov %0, %%cr3" : : "r"(addr));
}

static inline void enable_paging() {
    uint32_t cr0;
    __asm__ __volatile__("mov %%cr0, %0" : "=r"(cr0));
    cr0 |= 0x80000000;
    __asm__ __volatile__("mov %0, %%cr0" : : "r"(cr0));
}

void paging_switch_directory(page_directory_t* dir) {
    kernel_directory = dir;
    load_page_directory((uint32_t)dir);
}

void paging_init() {
    static page_directory_t kdir __attribute__((aligned(4096)));
    static page_table_t     ktable __attribute__((aligned(4096)));

    kernel_directory = &kdir;
    kernel_table     = &ktable;

    for (int i = 0; i < PAGE_ENTRIES; i++) {
        kdir.entries[i]   = 0;
        ktable.entries[i] = 0;
    }

    for (int i = 0; i < PAGE_ENTRIES; i++) {
        uint32_t addr = i * PAGE_SIZE;
        ktable.entries[i] = addr | PAGE_PRESENT | PAGE_RW;
    }

    kdir.entries[0] = ((uint32_t)&ktable) | PAGE_PRESENT | PAGE_RW;

    paging_switch_directory(&kdir);
    enable_paging();
}

void* paging_alloc_page() {
    return 0;
}

void paging_free_page(void* addr) {
    (void)addr;
}

void page_fault_handler_c() {
    volatile char* vga = (volatile char*)0xB8000;
    vga[0] = 'P';
    vga[1] = 0x4F;
    while (1) {
        __asm__ __volatile__("hlt");
    }
}

