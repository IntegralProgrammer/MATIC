#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PropertyEnforcer:
	def __init__(self, props):
		self.properties = props
		self.norepeat_vars = {}
	
	def enforce_norepeat(self, port_name, port_val):
		if port_name not in self.norepeat_vars:
			self.norepeat_vars[port_name] = []
		
		if port_val not in self.norepeat_vars[port_name]:
			self.norepeat_vars[port_name].append(port_val)
		
		else:
			return ('norepeat', port_name)
	
	def do_enforce(self, prop_type, port_name, port_val):
		if prop_type == 'norepeat':
			return self.enforce_norepeat(port_name, port_val)
	
	def enforce(self, input_signal):
		if self.properties == None:
			return []
		enforce_results = []
		for port in self.properties:
			port_enforce_results = []
			for prp in self.properties[port]:
				#Enforce the property
				res = self.do_enforce(prp, port, input_signal[port])
				if res != None:
					enforce_results.append(res)
		
		return enforce_results
	
