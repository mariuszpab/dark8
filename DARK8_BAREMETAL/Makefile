all: os.img

bootloader/boot.bin: bootloader/boot.asm
	nasm -f bin bootloader/boot.asm -o bootloader/boot.bin

bootloader/stage2.bin: bootloader/stage2.asm
	nasm -f bin bootloader/stage2.asm -o bootloader/stage2.bin

kernel/kernel.o: kernel/kernel.c
	i686-elf-gcc -ffreestanding -m32 -c kernel/kernel.c -o kernel/kernel.o

kernel/kernel_asm.o: kernel/kernel.asm
	nasm -f elf32 kernel/kernel.asm -o kernel/kernel_asm.o

kernel.bin: kernel/kernel.o kernel/kernel_asm.o
	i686-elf-ld -T kernel/linker.ld -nostdlib -o kernel.bin kernel/kernel.o kernel/kernel_asm.o

os.img: bootloader/boot.bin bootloader/stage2.bin kernel.bin
	dd if=/dev/zero of=os.img bs=512 count=2880
	dd if=bootloader/boot.bin   of=os.img bs=512 seek=0 conv=notrunc
	dd if=bootloader/stage2.bin of=os.img bs=512 seek=1 conv=notrunc
	dd if=kernel.bin            of=os.img bs=512 seek=10 conv=notrunc

clean:
	rm -f bootloader/*.bin
	rm -f kernel/*.o
	rm -f kernel.bin os.img

run:
	qemu-system-i386 -hda os.img

