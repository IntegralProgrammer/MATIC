#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Usage: python analyze_data_taint.py PROGRAM_GRAPH.json COMPILED_PROGRAM.json

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

#Enter the main loop
while True:
	#Prompt with a shell for event generation
	do_event = raw_input("Event Shell (Taint Analysis)>")
	#Allow blank lines for no input
	if do_event == "":
		continue
	
	if do_event in PROGRAM_GRAPH['input_nodes']:
		#Keep track of tainted system outputs
		tainted_outputs = []
		
		#Keep track of the returned values from each node
		node_returns_table = {}
		
		#First event receives no params
		first_event = True
		
		for op in COMPILED_PROGRAM[do_event]:
			node_name = op['node_name']
			print "Testing " + str(node_name)
			if first_event:
				#node_returns_table[node_name] = INPUT_NODES[node_name].node_method()
				#Input tainted data
				node_returns_table[node_name] = True
				first_event = False
				continue
			
			ports_template = op['input_nodeports']
			print "Resolving " + str(ports_template) + "..."
			#Resolve the values to be sent to the input ports of this node
			ports_resolved = {}
			for portkey in ports_template:
				ports_resolved[portkey] = node_returns_table[ports_template[portkey]]
			
			#Test the operation
			if node_name in PROGRAM_GRAPH['processing_nodes']:
				#node_returns_table[node_name] = PROCESSING_NODES[node_name].node_method(ports_resolved)
				#Check for the 'untaint' property
				if 'untaint' in PROGRAM_GRAPH['processing_nodes'][node_name]:
					if PROGRAM_GRAPH['processing_nodes'][node_name]['untaint'] == True:
						#Node returns untainted data
						node_returns_table[node_name] = False
					else:
						#Check if we have received tainted data, initially assume not
						node_returns_table[node_name] = False
						for prt in ports_resolved:
							if ports_resolved[prt] == True:
								node_returns_table[node_name] = True
				else:
					#Check if we have received tainted data, initally assume not
					node_returns_table[node_name] = False
					for prt in ports_resolved:
						if ports_resolved[prt] == True:
							node_returns_table[node_name] = True


			elif node_name in PROGRAM_GRAPH['output_nodes']:
				#node_returns_table[node_name] = OUTPUT_NODES[node_name].node_method(ports_resolved)
				#Check for the 'untaint' property
				if 'untaint' in PROGRAM_GRAPH['output_nodes'][node_name]:
					if PROGRAM_GRAPH['output_nodes'][node_name]['untaint'] == True:
						#Node returns untainted data
						node_returns_table[node_name] = False
					else:
						#Check if we have received tainted data, initally assume not
						node_returns_table[node_name] = False
						for prt in ports_resolved:
							if ports_resolved[prt] == True:
								node_returns_table[node_name] = True
				else:
					#Check if we have received tainted data, initally assume not
					node_returns_table[node_name] = False
					for prt in ports_resolved:
						if ports_resolved[prt] == True:
							node_returns_table[node_name] = True
				
				#Is this node's output is tainted?
				if node_returns_table[node_name] == True:
					tainted_outputs.append(node_name)
		
		#Alert the user
		if len(tainted_outputs) == 0:
			print "===================================================="
			print "Execellent news! No outputs appear to be tainted"
			print "===================================================="
		
		else:
			print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
			print "Please beware, the following outputs are tainted:"
			for t_out in tainted_outputs:
				print t_out
			print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		
	else:
		print "ERROR: No input node matching " + do_event
