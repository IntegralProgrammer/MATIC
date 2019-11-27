#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converts a hexadecimal representation of a binary string to an
actual binary string
"""
class NODE__hex_to_bytes:
	def __init__(self):
		pass
	
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None
		
		input_str = signal_in['default']
		bin_str = ""
		for hc_i in range(0,len(input_str), 2):
			hc = input_str[hc_i: hc_i + 2]
			bin_str += chr(int(hc, 16))
		
		return bin_str
