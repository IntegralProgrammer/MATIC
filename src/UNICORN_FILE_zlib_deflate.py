#!/usr/bin/python

from unicorn import *
from unicorn.arm_const import *

#Code to be emulated
f_text = open('UNICORN_ZLIB_DEFLATE/text.bin', 'rb')
TEXT_SECTION = f_text.read()
f_text.close()

#Data section of program
f_data = open('UNICORN_ZLIB_DEFLATE/data.bin', 'rb')
DATA_SECTION = f_data.read()
f_data.close()

f_rodata = open('UNICORN_ZLIB_DEFLATE/rodata.bin', 'rb')
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
	mu.mem_write(0x8018, TEXT_SECTION) #.text section
	mu.mem_write(0x250b0, DATA_SECTION) #.data section
	mu.mem_write(0x12400, RODATA_SECTION) #.rodata section
	
	#Add the input data to the compressor
	compressor_input = signal_in['default']
	mu.mem_write(0x250b4, compressor_input)
	
	#Begin emulation
	mu.emu_start(0x827c, 0x832c)
	
	#Retrieve data
	compressed_buffer = mu.mem_read(0x250e8, 50)
	compressed_length = mu.mem_read(0x259b0, 4)
	
	#Format compressed_length to a Python integer format
	integer_length = int(str(compressed_length).encode('hex'))
	
	#Slice the compressed data, forget the rest
	return str(compressed_buffer)[0:integer_length]
	
	
