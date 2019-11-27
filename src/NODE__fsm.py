#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements a Finite State Machine (FSM)
"""

class NODE__fsm:
	def __init__(self, t_table, i_state):
		"""
		Transition table must be defined as follows:
		{
			"state_a" : {"next_states" : {
								"signal_1" : "state_b",
								"signal_2" : "state_c"
							},
							"output" : BITSTRING
						},
			"state_b" : {"next_states" : {
								"signal_1" : "state_a",
								"signal_2" : "state_c"
							},
							"output" : BITSTRING
						},
			"state_c" : {"next_states" : {
								"signal_1" : "state_b",
								"signal_2" : "state_a"
							},
							"output" : BITSTRING
						}
		}
		"""
		self.transition_table = t_table
		self.__current_state = i_state #Begin at initial state
		
	
	def node_method(self, signal_in):
		"""
		Transitions state and produces appropriate output.
		"""
		
		if signal_in['default'] == None:
			return None
		
		next_state = self.transition_table[self.__current_state]['next_states'][str(signal_in['default'])]
		#transition states
		self.__current_state = next_state
		#get output from newly transitioned state
		this_output = self.transition_table[self.__current_state]['output']
		return this_output
		
