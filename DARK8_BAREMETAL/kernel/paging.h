#ifndef D8_PAGING_H
#define D8_PAGING_H

#include <stdint.h>

#define PAGE_SIZE     4096
#define PAGE_ENTRIES  1024

#define PAGE_PRESENT  0x1
#define PAGE_RW       0x2

typedef struct {
    uint32_t entries[PAGE_ENTRIES];
} page_table_t;

typedef struct {
    uint32_t entries[PAGE_ENTRIES];
} page_directory_t;

void paging_init();
void paging_switch_directory(page_directory_t* dir);
void* paging_alloc_page();
void paging_free_page(void* addr);
void page_fault_handler_c();

#endif

