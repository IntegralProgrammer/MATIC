#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Returns to hex representation of a string
"""

class NODE__str_to_hex:
	def __init__(self):
		pass
	
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None
		
		return str(signal_in['default']).encode('hex')
