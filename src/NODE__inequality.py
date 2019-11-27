#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This node can be used for implementing selection (if statements). If
the input 'input_a' is not equal to the input 'input_b', then the value
'input_c' is propagated forward through the network. If they are not
equal, the None value is propagated forward causing all downstream nodes
to be effectively abscent.
"""

class NODE__inequality:
	def __init__(self):
		pass
	
	def node_method(self, signal_in):
		if signal_in['input_a'] == None or signal_in['input_b'] == None or signal_in['input_c'] == None:
			return None
		
		if signal_in['input_a'] != signal_in['input_b']:
			return signal_in['input_c']
		else:
			return None
		
