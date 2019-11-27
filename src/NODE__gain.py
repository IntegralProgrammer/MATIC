#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NODE__gain:
	def __init__(self, k_value):
		self.gain_value = k_value
	
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None

		return self.gain_value * signal_in['default']
