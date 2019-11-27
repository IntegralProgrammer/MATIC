#!/usr/bin/python

from unicorn import *
from unicorn.arm_const import *

#Code to be emulated
f_text = open('UNICORN_ZLIB_INFLATE/text.bin', 'rb')
TEXT_SECTION = f_text.read()
f_text.close()

#Data section of program
f_data = open('UNICORN_ZLIB_INFLATE/data.bin', 'rb')
DATA_SECTION = f_data.read()
f_data.close()

f_rodata = open('UNICORN_ZLIB_INFLATE/rodata.bin', 'rb')
RODATA_SECTION = f_rodata.read()
f_rodata.close()

def node_method(signal_in):
	#Create the QEMU ARM CPU
	mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)

	#Map 4MB program memory
	mu.mem_map(0x0000, 4 * 1024 * 1024)

	#Setup stack pointer
	mu.reg_write(UC_ARM_REG_SP, 0x00 + 8 * 1024)
	
	#Load program into memory
	mu.mem_write(0x8018, TEXT_SECTION)
	mu.mem_write(0x22e08, DATA_SECTION)
	mu.mem_write(0x10088, RODATA_SECTION)
	
	
	#Add in the compressed data
	compressed_buffer = signal_in['default']
	mu.mem_write(0x22e0c, compressed_buffer)
	
	#Begin emulation
	mu.emu_start(0x827c, 0x8314)
	
	#Retrieve data
	inflated_data = mu.mem_read(0x23698, 50)
	
	return str(inflated_data)
