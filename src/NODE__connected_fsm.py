#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements a Finite State Machine (FSM) which shares state with all
other finite state machines in this group.
"""

class NODE__connected_fsm:
	def __init__(self, t_table, i_state):
		self.transition_table = t_table
		self.__current_state = i_state #Begin at initial state
		self.linked_machines = []

	def link_machine(self, lm):
		self.linked_machines.append(lm)
		
	def node_method(self, signal_in):
		if signal_in['default'] == None:
			return None
		
		#Do the state transition for this node
		next_state = self.transition_table[self.__current_state]['next_states'][str(signal_in['default'])]
		#transition states
		self.__current_state = next_state
		#get output from newly transitioned state
		this_output = self.transition_table[self.__current_state]['output']
		
		#Also update all other linked FSMs
		for m in self.linked_machines:
			m.__current_state = self.__current_state
		
		return this_output
