#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Usage: python run_application.py PROGRAM_GRAPH.json

"""

import sys
import json

import networkx as nx

from node_creator import construct_node
import graph_functions

PROGRAM_GRAPH_FILE = sys.argv[1]

#Load the program graph
f_graph = open(PROGRAM_GRAPH_FILE, 'r')
PROGRAM_GRAPH = json.loads(f_graph.read())
f_graph.close()

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

#...output nodes
OUTPUT_NODES = {}
for node_key in PROGRAM_GRAPH['output_nodes']:
	node_type = PROGRAM_GRAPH['output_nodes'][node_key]['type']
	node_init_args = PROGRAM_GRAPH['output_nodes'][node_key]['init_args']
	OUTPUT_NODES[node_key] = construct_node(node_type, node_init_args)

#...linked nodes
LINKED_NODES = {}
for node_key in PROGRAM_GRAPH['linked_nodes']:
	node_type = PROGRAM_GRAPH['linked_nodes'][node_key]['type']
	node_init_args = PROGRAM_GRAPH['linked_nodes'][node_key]['init_args']
	LINKED_NODES[node_key] = construct_node(node_type, node_init_args)

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

#Get a networkx model of the graph
NX_MODEL = graph_functions.make_nx_digraph(PROGRAM_GRAPH)

#Enter the main loop
"""
while True:
	#For each input event
	for ev_input in INPUT_NODES:
		input_node_value = INPUT_NODES[ev_input].node_method()
	
		#Propagate through network
		#...get nodes which this input_node_value should be fed forward to
		feedforward = PROGRAM_GRAPH['input_nodes'][ev_input]['feedforward']
		#...propagate forward
		for next_node in feedforward:
			pass #TODO: implement feedforward
	
		#Get outputs
	
"""

#	Algorithm works by going through all nodes...
#	...each node takes its input(s)...
#	...processes it through its function...
#	...latches it to its output...
#	...only intermediate and output nodes have this latching
#		functionality...
#	...we must wait for an input event and only accept new input events
#		once propagation is complete...
#
#	...but how do we know when propagation is complete?
#	...we know this as all ends of the path of the "tagged" input
#		signal have reached deadends.

while True:
	#Prompt with a shell for event generation
	do_event = raw_input("Event Shell>")
	#Allow blank lines for no input
	if do_event == "":
		continue
		
	#Match do_event with an input node
	if do_event in INPUT_NODES:
		print "Triggering event " + do_event
		#Call this node's method
		event_return = INPUT_NODES[do_event].node_method()
		#Now get the subgraph of nodes which are affected by the...
		#...triggering of this input node
		affected_subgraph = graph_functions.get_affected_subgraph(NX_MODEL, do_event)
		
		#Build a table of all node methods along this path and their...
		#...return values
		
		relevant_nodes = nx.nodes(affected_subgraph)
		node_returns_table = {}
		for rn in relevant_nodes:
			node_returns_table[str(rn)] = {'done' : False, 'value' : None}
			
		print node_returns_table
		
		incomplete_returns_table = True
		while incomplete_returns_table:
			#Populate the returns table
			for rn in node_returns_table:
				#Do we need to execute node_method() for rn?
				if node_returns_table[rn]['done'] == True:
					continue
				#Can we execute the node_method() for rn?
				#If it has dependencies, have those been satisfied?
				print "Testing if " + str(rn) + " can be executed."
				preds = affected_subgraph.predecessors(rn)
				#If no predecessors then this processing node receives
				#Input directly from Input Node do_event
				if len(preds) == 0:
					print "Feeding input directly"
					#Determine which port this input should be sent to
					#...lookup the feedforward configuration for Input Node 'do_event'
					ff_conf = PROGRAM_GRAPH['input_nodes'][do_event]['feedforward']
					for ff_node in ff_conf:
						if ff_node['name'] == rn:
							#Get the port which this event must be sent to
							ff_port = ff_node['port']
							break
					node_returns_table[rn]['value'] = PROCESSING_NODES[rn].node_method({ff_port : event_return})
					node_returns_table[rn]['done'] = True
					continue
				can_run = True
				for p in preds:
					print "Checking predecessor " + str(p)
					if node_returns_table[str(p)]['done'] == False:
						#We cannot run node_method() for rn
						#...therefore break and try another rn
						can_run = False
						break
				if not can_run:
					continue
				
				#Once this point is reached we may execute node_method() for rn
				print "Executing " + str(rn)
				
				#Get the input for rn
				#if len(preds) > 1:
				#	print "RACE CONDITION"
				
				#rn_input = node_returns_table[preds[0]]['value']
				#Get the port which this data must be fed-forward into
				
				forward_rn = {}
				for p in preds:
					#Lookup the predecessor, 'p'...
					#Lookup p's feedforward configuration for rn...
					p_feedforward = PROGRAM_GRAPH['processing_nodes'][p]['feedforward']
					for ff in p_feedforward:
						if ff['name'] == rn:
							#If at any point two or more predecessors feed into
							#...the same node port ALERT OF THE RACE CONDITION!
							if ff['port'] in forward_rn:
								print "RACE CONDITION!"
							
							#Take the output from 'p'
							#And add it to port-value dictionary
							#...which will be sent to the feedforward node								
							forward_rn[ff['port']] = node_returns_table[p]['value']

				print forward_rn
				
				
				#node_returns_table[str(rn)]['value'] = PROCESSING_NODES[str(rn)].node_method()
				#Decide if rn is a PROCESSING_NODE or an OUTPUT_NODE
				if rn in PROCESSING_NODES:
					node_returns_table[str(rn)]['value'] = PROCESSING_NODES[str(rn)].node_method(forward_rn)
				elif rn in OUTPUT_NODES:
					node_returns_table[str(rn)]['value'] = OUTPUT_NODES[str(rn)].node_method(forward_rn)
				
				node_returns_table[str(rn)]['done'] = True
			
			#Check if the returns table has been completed
			incomplete_returns_table = False
			for rn in node_returns_table:
				if node_returns_table[rn]['done'] == False:
					incomplete_returns_table = True
		
		print node_returns_table
		
	else:
		print "ERROR: No input node matching " + do_event

