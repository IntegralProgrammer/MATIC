#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


"""
Returns a networkx DiGraph representation of the program flow
from its dictionnary representation.
"""
def make_nx_digraph(graph_di):
	#Create the directed graph
	G = nx.DiGraph()
	#Add Input Nodes to NX graph
	for input_node in graph_di['input_nodes']:
		print input_node
		G.add_node(input_node)
	
	#Add Processing Nodes to NX graph
	for processing_node in graph_di['processing_nodes']:
		print processing_node
		G.add_node(processing_node)
	
	#Add Output Nodes to NX graph
	for output_node in graph_di['output_nodes']:
		print output_node
		G.add_node(output_node)


	#Add 'feedforward' edges for Input Nodes
	for input_node in graph_di['input_nodes']:
		for feedforward_node in graph_di['input_nodes'][input_node]['feedforward']:
			print input_node + " --> " + feedforward_node['name']
			G.add_edge(input_node, feedforward_node['name'])

	#Add 'feedforward' edges for Processing Nodes
	for processing_node in graph_di['processing_nodes']:
		for feedforward_node in graph_di['processing_nodes'][processing_node]['feedforward']:
			print processing_node + " --> " + feedforward_node['name']
			G.add_edge(processing_node, feedforward_node['name'])
			
	return G


"""
Returns the subgraph (from graph) of nodes which are affected by a
triggering of input_node.

This is needed for determining which nodes the event 'ripple' must be
propagated to.
"""
def get_affected_subgraph(graph, input_node):
	desc = nx.descendants(graph, input_node)
	sub_g = graph.subgraph(desc)
	return sub_g
