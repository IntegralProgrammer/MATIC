#!/usr/bin/python

from unicorn import *
from unicorn.arm_const import *

crypto_sign_BYTES = 64 #Defined in tweetnacl.h

#Code to be emulated
f_text = open('UNICORN_NACL_SIGN/text.bin', 'rb')
TEXT_SECTION = f_text.read()
f_text.close()

#Data section of program
f_data = open('UNICORN_NACL_SIGN/data.bin', 'rb')
DATA_SECTION = f_data.read()
f_data.close()

f_rodata = open('UNICORN_NACL_SIGN/rodata.bin', 'rb')
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


	#Clear input message buffer
	empty_str = chr(0)*50
	mu.mem_write(0x1e378, empty_str)

	#Input message to sign
	text_input_msg = signal_in['default']
	mu.mem_write(0x1e378, text_input_msg)

	#Private key for signing the message
	secret_key = signal_in['secret_key']
	mu.mem_write(0x1e338, secret_key)

	#Run the CPU to generate the cryptographically signed message
	mu.emu_start(0x827c, 0x82d8)

	#Retrieve the signed message from memory
	signed_message = mu.mem_read(0x1e954, 50 + crypto_sign_BYTES)

	#Returned the signed_message
	return signed_message

