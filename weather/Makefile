all: hack.bin

hack.ihx:
	sdcc --code-loc 0x0E00 hack.c

hack.bin: hack.ihx
	objcopy -Iihex -Obinary hack.ihx hack.bin
	rm -f hack.asm hack.lk hack.lst hack.map hack.mem hack.rel hack.rst hack.sym hack.ihx

clean:
	rm -f hack.bin hack.ihx