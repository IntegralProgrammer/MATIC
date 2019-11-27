#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NODE__adder:
	def __init__(self):
		pass
	
	def node_method(self, signal_in):
		if signal_in['input_a'] == None or signal_in['input_b'] == None:
			return None

		return signal_in['input_a'] + signal_in['input_b']
