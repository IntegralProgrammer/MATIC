#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NODE__printer:
	def __init__(self):
		pass
		
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None	
		
		print "--- BEGIN OUTPUT ---"
		print str(signal_in['default'])
		print "--- END OUTPUT ---"
