#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NODE__xor:
	def __init__(self):
		pass
	
	def node_method(self, signal_in):
		if signal_in['input_a'] == None or signal_in['input_b'] == None:
			return None
			
		input_a = str(signal_in['input_a'])
		input_b = str(signal_in['input_b'])
		#Thanks to https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
		return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(input_a, input_b))
		
