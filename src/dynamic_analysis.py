#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Usage: python dynamic_analysis.py PROGRAM_GRAPH.json COMPILED_PROGRAM.json

"""

import sys
import json

from node_creator import construct_node
from property_enforcer import PropertyEnforcer

PROGRAM_GRAPH_FILE = sys.argv[1]
COMPILED_PROGRAM_FILE = sys.argv[2]

#Load the program graph
f_graph = open(PROGRAM_GRAPH_FILE, 'r')
PROGRAM_GRAPH = json.loads(f_graph.read())
f_graph.close()


PROPERTY_ENFORCERS = {}

#Build the network
#...input nodes
INPUT_NODES = {}
for node_key in PROGRAM_GRAPH['input_nodes']:
	node_type = PROGRAM_GRAPH['input_nodes'][node_key]['type']
	node_init_args = PROGRAM_GRAPH['input_nodes'][node_key]['init_args']
	INPUT_NODES[node_key] = construct_node(node_type, node_init_args)

#...processing nodes
PROCESSING_NODES = {}
for node_key in PROGRAM_GRAPH['processing_nodes']:
	node_type = PROGRAM_GRAPH['processing_nodes'][node_key]['type']
	node_init_args = PROGRAM_GRAPH['processing_nodes'][node_key]['init_args']
	PROCESSING_NODES[node_key] = construct_node(node_type, node_init_args)
	if 'properties' in PROGRAM_GRAPH['processing_nodes'][node_key]:
		PROPERTY_ENFORCERS[node_key] = PropertyEnforcer(PROGRAM_GRAPH['processing_nodes'][node_key][properties])
	else:
		PROPERTY_ENFORCERS[node_key] = PropertyEnforcer(None)

#...output nodes
OUTPUT_NODES = {}
for node_key in PROGRAM_GRAPH['output_nodes']:
	node_type = PROGRAM_GRAPH['output_nodes'][node_key]['type']
	node_init_args = PROGRAM_GRAPH['output_nodes'][node_key]['init_args']
	OUTPUT_NODES[node_key] = construct_node(node_type, node_init_args)
	if 'properties' in PROGRAM_GRAPH['output_nodes'][node_key]:
		PROPERTY_ENFORCERS[node_key] = PropertyEnforcer(PROGRAM_GRAPH['output_nodes'][node_key]['properties'])
	else:
		PROPERTY_ENFORCERS[node_key] = PropertyEnforcer(None)

#...linked nodes
LINKED_NODES = {}
for node_key in PROGRAM_GRAPH['linked_nodes']:
	node_type = PROGRAM_GRAPH['linked_nodes'][node_key]['type']
	node_init_args = PROGRAM_GRAPH['linked_nodes'][node_key]['init_args']
	LINKED_NODES[node_key] = construct_node(node_type, node_init_args)
	if 'properties' in PROGRAM_GRAPH['linked_nodes'][node_key]:
		PROPERTY_ENFORCERS[node_key] = PropertyEnforcer(properties)
	else:
		PROPERTY_ENFORCERS[node_key] = PropertyEnforcer(None)

#Setup the link(s) for linked nodes
for node_key in PROGRAM_GRAPH['linked_nodes']:
	selected_node = LINKED_NODES[node_key]
	#...build links
	for linked_node in PROGRAM_GRAPH['linked_nodes'][node_key]['linked']:
		selected_node.link_machine(LINKED_NODES[linked_node])

#Add LINKED_NODES into PROCESSING_NODES
for ln in LINKED_NODES:
	PROCESSING_NODES[ln] = LINKED_NODES[ln]	

for ln in PROGRAM_GRAPH['linked_nodes']:
	PROGRAM_GRAPH['processing_nodes'][ln] = PROGRAM_GRAPH['linked_nodes'][ln]	


#Load the compiled program
f_compiled = open(COMPILED_PROGRAM_FILE, 'r')
COMPILED_PROGRAM = json.loads(f_compiled.read())
f_compiled.close()

#Enter the main loop
while True:
	#Prompt with a shell for event generation
	do_event = raw_input("Event Shell (Dynamic Analysis)>")
	#Allow blank lines for no input
	if do_event == "":
		continue
	
	if do_event in INPUT_NODES:
		#Trigger this event...
		
		#Keep track of the returned values from each node
		node_returns_table = {}
		
		#First event receives no params
		first_event = True
		
		for op in COMPILED_PROGRAM[do_event]:
			node_name = op['node_name']
			print "Running " + str(node_name)
			if first_event:
				node_returns_table[node_name] = INPUT_NODES[node_name].node_method()
				first_event = False
				continue
			
			ports_template = op['input_nodeports']
			print "Resolving " + str(ports_template) + "..."
			#Resolve the values to be sent to the input ports of this node
			ports_resolved = {}
			for portkey in ports_template:
				ports_resolved[portkey] = node_returns_table[ports_template[portkey]]
			
			#Run the operation
			if node_name in PROCESSING_NODES:
				node_returns_table[node_name] = PROCESSING_NODES[node_name].node_method(ports_resolved)
			elif node_name in OUTPUT_NODES:
				node_returns_table[node_name] = OUTPUT_NODES[node_name].node_method(ports_resolved)
		
			#Enforce properties
			prop_check = PROPERTY_ENFORCERS[node_name].enforce(ports_resolved)
			
			for pc in prop_check:
				print "!!! Violation of property " + pc[0] + " on port " + pc[1] + " on node " + node_name + "!!!"
		
	else:
		print "ERROR: No input node matching " + do_event
