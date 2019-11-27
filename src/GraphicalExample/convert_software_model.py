#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from lxml import etree

import resolve_init_args

#Object describing program graph, to be JSON dumped
PROGRAM_GRAPH = {}
PROGRAM_GRAPH["input_nodes"] = {}
PROGRAM_GRAPH["processing_nodes"] = {}
PROGRAM_GRAPH["output_nodes"] = {}
PROGRAM_GRAPH["linked_nodes"] = {}

#Read the XML file
#f_xml = open('software_model.xml', 'r')
f_xml = open(sys.argv[1], 'r')
XML_DOCUMENT = f_xml.read()
f_xml.close()

tree = etree.fromstring(XML_DOCUMENT)

processing_nodes = tree.xpath("/mxGraphModel/root/Rect/@label")
input_nodes = tree.xpath("/mxGraphModel/root/Shape/mxCell[@style='actor']/../@label")
output_nodes = tree.xpath("/mxGraphModel/root/Shape/mxCell[@style='triangle']/../@label")
feedforward_source_links = tree.xpath("/mxGraphModel/root/Connector/mxCell[@style='straightConnector']/@source")
feedforward_target_links = tree.xpath("/mxGraphModel/root/Connector/mxCell[@style='straightConnector']/@target")

print "Input Nodes"
print "-----------"
print input_nodes

print "============================"


print "Processing Nodes"
print "----------------"
print processing_nodes

print "============================"

print "Output Nodes"
print "------------"
print output_nodes

print "============================"


#Add in Input Nodes
for input_n in input_nodes:
	#Get the type of node
	this_type = str(input_n).split(':')[0]
	#Get the name of node
	this_name = str(input_n).split(':')[1]
	#construct dictionary of processing nodes
	this_node = {}
	this_node['type'] = this_type
	this_node['init_args'] = []
	this_node['feedforward'] = []
	PROGRAM_GRAPH['input_nodes'][this_name] = this_node

#Add in Processing Nodes
for pn in processing_nodes:
	#Get the type of node
	this_type = str(pn).split(':')[0]
	#Get the name of node
	this_name = str(pn).split(':')[1]
	#construct dictionary of processing nodes
	this_node = {}
	this_node['type'] = this_type
	this_node['init_args'] = resolve_init_args.resolve_type(this_type, this_name)
	this_node['feedforward'] = []
	PROGRAM_GRAPH['processing_nodes'][this_name] = this_node

#Add in Output Nodes
for out_n in output_nodes:
	#Get the type of node
	this_type = str(out_n).split(':')[0]
	#Get the name of node
	this_name = str(out_n).split(':')[1]
	#construct dictionary of processing nodes
	this_node = {}
	this_node['type'] = this_type
	this_node['init_args'] = []
	this_node['feedforward'] = []
	PROGRAM_GRAPH['output_nodes'][this_name] = this_node

print feedforward_source_links
print feedforward_target_links

feedforward_links = []
for i in range(0,len(feedforward_source_links)):
	feedforward_links.append((feedforward_source_links[i], feedforward_target_links[i]))

print feedforward_links

#Resolve feedforward_links
for src,dst in feedforward_links:
	processing_resolved_src = tree.xpath("/mxGraphModel/root/Rect[@id='" + str(src) + "']/@label")
	input_resolved_src = tree.xpath("/mxGraphModel/root/Shape[@id='" + str(src) + "']/@label")
	if len(processing_resolved_src) == 1:
		resolved_src = processing_resolved_src[0]
	elif len(input_resolved_src) == 1:
		resolved_src = input_resolved_src[0]
	
	resolved_src_name = resolved_src.split(':')[1]
	
	processing_resolved_dst = tree.xpath("/mxGraphModel/root/Rect[@id='" + str(dst) + "']/@label")
	output_resolved_dst = tree.xpath("/mxGraphModel/root/Shape[@id='" + str(dst) + "']/@label")
	if len(processing_resolved_dst) == 1:
		resolved_dst = processing_resolved_dst[0]
	elif len(output_resolved_dst) == 1:
		resolved_dst = output_resolved_dst[0]
	
	resolved_dst_name = resolved_dst.split(':')[1]
	
	
	#print "From: " + str(src)
	print "From: " + str(resolved_src_name)
	#print "To: " + str(dst)
	print "To: " + str(resolved_dst_name)
	
	#Add this feedforward link to PROGRAM_GRAPH
	if resolved_src_name in PROGRAM_GRAPH['input_nodes']:
		PROGRAM_GRAPH['input_nodes'][resolved_src_name]['feedforward'].append({"name" : resolved_dst_name, "port" : "default"})
	elif resolved_src_name in PROGRAM_GRAPH['processing_nodes']:
		PROGRAM_GRAPH['processing_nodes'][resolved_src_name]['feedforward'].append({"name" : resolved_dst_name, "port" : "default"})
	
#Write to file
f_json = open(sys.argv[2], 'w')
f_json.write(json.dumps(PROGRAM_GRAPH))
f_json.close()
