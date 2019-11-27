#!/usr/bin/python

from unicorn import *
from unicorn.arm_const import *

crypto_sign_BYTES = 64 #Defined in tweetnacl.h

#Code to be emulated
f_text = open('UNICORN_NACL_VERIFY/text.bin', 'rb')
TEXT_SECTION = f_text.read()
f_text.close()

#Data section of program
f_data = open('UNICORN_NACL_VERIFY/data.bin', 'rb')
DATA_SECTION = f_data.read()
f_data.close()

f_rodata = open('UNICORN_NACL_VERIFY/rodata.bin', 'rb')
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
	mu.mem_write(0x1e310, DATA_SECTION) #.data section
	mu.mem_write(0xdb30, RODATA_SECTION) #.rodata section

	#Public key
	public_key = signal_in['public_key']
	mu.mem_write(0x1e318, public_key)


	#Signed message to verify
	wire_input = signal_in['default']

	#Run the CPU to begin the program
	mu.emu_start(0x827c, 0x82d8)

	#Add the signed message to verify
	mu.mem_write(0x1e954, wire_input)

	#Continue with verification
	mu.emu_start(0x82d8, 0x8314)

	#Return if this message is valid or not
	verification_status = mu.mem_read(0x1e3e8, 4)
	return verification_status
