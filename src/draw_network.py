#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import networkx as nx
import pylab as plt

import graph_functions

#Create the directed graph
#G = nx.DiGraph()

PROGRAM_GRAPH_FILE = sys.argv[1]

#Load the program graph
f_graph = open(PROGRAM_GRAPH_FILE, 'r')
PROGRAM_GRAPH = json.loads(f_graph.read())
f_graph.close()

G = graph_functions.make_nx_digraph(PROGRAM_GRAPH)

"""
#Add Input Nodes to NX graph
for input_node in PROGRAM_GRAPH['input_nodes']:
	print input_node
	G.add_node(input_node)
	
#Add Processing Nodes to NX graph
for processing_node in PROGRAM_GRAPH['processing_nodes']:
	print processing_node
	G.add_node(processing_node)
	
#Add Output Nodes to NX graph
for output_node in PROGRAM_GRAPH['output_nodes']:
	print output_node
	G.add_node(output_node)


#Add 'feedforward' edges for Input Nodes
for input_node in PROGRAM_GRAPH['input_nodes']:
	for feedforward_node in PROGRAM_GRAPH['input_nodes'][input_node]['feedforward']:
		print input_node + " --> " + feedforward_node
		G.add_edge(input_node, feedforward_node)

#Add 'feedforward' edges for Processing Nodes
for processing_node in PROGRAM_GRAPH['processing_nodes']:
	for feedforward_node in PROGRAM_GRAPH['processing_nodes'][processing_node]['feedforward']:
		print processing_node + " --> " + feedforward_node
		G.add_edge(processing_node, feedforward_node)

"""

#Simply draw the graph if no source node is specified
if len(sys.argv) == 2:
	pos = nx.spring_layout(G)
	#nx.draw(G, pos)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_nodes(G, pos, shape='s', node_color='k')
	nx.draw_networkx_labels(G, pos, font_size=20, font_color='c')
	plt.show()
	
elif len(sys.argv) == 3:
	SOURCE_NODE = sys.argv[2]
	affected_nodes = nx.descendants(G, SOURCE_NODE)
	pos = nx.spring_layout(G)
	#nx.draw(G, pos)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_nodes(G, pos, nodelist=affected_nodes, shape='s', node_color='r')
	nx.draw_networkx_labels(G, pos, font_size=20, font_color='c')
	plt.show()

