#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converts any data to its string representation
"""

class NODE__to_string:
	def __init__(self):
		pass
	
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None
		
		return str(signal_in['default'])
