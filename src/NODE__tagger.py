#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NODE__tagger:
	def __init__(self, t_msg):
		self.tag_message = t_msg
	
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None
		
		return "Tagged:" + str(self.tag_message) + ":" + str(signal_in['default'])
	
	
