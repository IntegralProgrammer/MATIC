#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Usage: python analyze_application_timing.py PROGRAM_GRAPH.json COMPILED_PROGRAM.json

"""

import sys
import json

PROGRAM_GRAPH_FILE = sys.argv[1]
COMPILED_PROGRAM_FILE = sys.argv[2]

#Load the program graph
f_graph = open(PROGRAM_GRAPH_FILE, 'r')
PROGRAM_GRAPH = json.loads(f_graph.read())
f_graph.close()


#Add LINKED_NODES into PROCESSING_NODES
for ln in PROGRAM_GRAPH['linked_nodes']:
	PROGRAM_GRAPH['processing_nodes'][ln] = PROGRAM_GRAPH['linked_nodes'][ln]	


#Load the compiled program
f_compiled = open(COMPILED_PROGRAM_FILE, 'r')
COMPILED_PROGRAM = json.loads(f_compiled.read())
f_compiled.close()

#Load required timing information
f_timing = open('TIMING_INFO.json','r')
TIMING_INFO = json.loads(f_timing.read())
f_timing.close()

#Enter the main loop
while True:
	#Prompt with a shell for event generation
	do_event = raw_input("Event Shell (Timing Analysis)>")
	#Allow blank lines for no input
	if do_event == "":
		continue
	
	if do_event in PROGRAM_GRAPH['input_nodes']:
		"""
		Dictionary maping output node triggered to trigger delay -
		'trigger delay' refers to the time it takes for this output node
		to be triggered after the given input node is triggered.
		"""
		output_timegraph = {}
		
		#Keep track of all elapsed time constants or time variables
		time_track = []
		
		#First assume constant time
		constant_time = True
		
		
		#First event receives no params
		first_event = True
		
		for op in COMPILED_PROGRAM[do_event]:
			node_name = op['node_name']
			print "Testing " + str(node_name)
			if first_event:
				#node_returns_table[node_name] = INPUT_NODES[node_name].node_method()
				first_event = False
				continue
			
			#Test the operation
			if node_name in PROGRAM_GRAPH['processing_nodes']:
				#node_returns_table[node_name] = PROCESSING_NODES[node_name].node_method(ports_resolved)
				#Get the node type
				node_type = PROGRAM_GRAPH['processing_nodes'][node_name]['type']

			elif node_name in PROGRAM_GRAPH['output_nodes']:
				#node_returns_table[node_name] = OUTPUT_NODES[node_name].node_method(ports_resolved)
				#Get the node type
				node_type = PROGRAM_GRAPH['output_nodes'][node_name]['type']
			
			#Get the timing information associated with this node type
			node_time = TIMING_INFO[node_type]
			
			if node_time['fixed'] == False:
				#No longer can it be said that this runs in constant time
				constant_time = False
			
			#Add the time variable or time constant
			time_track.append(node_time['var'])
			
			#If we have just simulated an output node, log the propagation delay
			if node_name in PROGRAM_GRAPH['output_nodes']:
				output_timegraph[node_name] = {"fixed" : constant_time, "var" : time_track}
			
				
		#Alert the user
		for node in output_timegraph:
			if output_timegraph[node]['fixed'] == True:
				print "===================================================="
				print "Output Node " + node  + " will output in constant time."
				print "This occurs after..."
				for cnst in output_timegraph[node]['var']:
					print cnst
				print "===================================================="
			else:
				print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				print "Output Node " + node + " will NOT output in constant time."
				print "This occurs after..."
				for cnst in output_timegraph[node]['var']:
					print cnst
				print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		
	else:
		print "ERROR: No input node matching " + do_event
