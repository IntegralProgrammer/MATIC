#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- BEGIN USER IMPORTS ---
import UNICORN_FILE_nacl_verify as unicorn_file
# --- END USER IMPORTS ---

"""
Ensures that a parameter 'in_param' can only be 'len_param' bytes long.
If it is of wrong type 'len_param' zeros are returned
If it is too long it is truncated
If it is too short it is padded with zeros
"""
def sanitize_parameter(in_param, len_param):
	#Assert that it is a string, if not return len_param in zeros
	if type(in_param) != str and type(in_param) != bytearray:
		return chr(0)*len_param
	
	#...at this point in_param is a string
	#...if it is of length len_param simply return it
	if len(in_param) == len_param:
		return in_param
	
	#...if it is greater than len_param truncate it
	if len(in_param) > len_param:
		return in_param[0:len_param]
	
	#...if it is less than len_param zero pad right side
	padded_param = in_param
	while len(padded_param) < len_param:
		padded_param += chr(0)
	
	return padded_param


class NODE__unicorn_nacl_verify:
	def __init__(self):
		self.__input_port_size = {}
		#Place Port Definitions Here
		# --- BEGIN USER PARAMS ---
		self.__input_port_size['default'] = 50 + 64
		self.__input_port_size['public_key'] = 32
		self.__output_port_size = 4
		# --- END USER PARAMS ---
		
	
	def node_method(self, signal_in):
		if signal_in['default'] == None or signal_in['public_key'] == None:
			return None
			
		#Validate signal_in
		clean_signal_in = {}
		for prt in self.__input_port_size:
			#Sanitize
			clean_signal_in[prt] = sanitize_parameter(signal_in[prt], self.__input_port_size[prt])
		
		#Call the node method from the unicorn file with the clean signal
		unicorn_ret = unicorn_file.node_method(clean_signal_in)
		
		#return validated data
		return sanitize_parameter(unicorn_ret, self.__output_port_size)
		
