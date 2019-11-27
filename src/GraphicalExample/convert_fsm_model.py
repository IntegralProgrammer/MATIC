#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

def convert_xml_fsm(node_name):
	filename = node_name + ".xml"
	f_xml = open(filename, 'r')
	XML_DOCUMENT = f_xml.read()
	f_xml.close()
	
	tree = etree.fromstring(XML_DOCUMENT)
	
	#Find the initial state
	initial_state = tree.xpath("/mxGraphModel/root/Shape/mxCell[@style='doubleEllipse']/../@label")
	
	if len(initial_state) == 0:
		print "[ERROR] Must define an initial state"
		return
		
	if len(initial_state) > 1:
		print "[ERROR] Must only have one initial state"
		return
	
	initial_state = initial_state[0]
	
	#Find all other states
	other_states = tree.xpath("/mxGraphModel/root/Shape/mxCell[@style='ellipse']/../@label")
	
	all_states = [initial_state] + other_states
	
	#Define the state machine to be passed as an init arg, resolve outputs
	STATEMACHINE = {}
	for st in all_states:
		state_name = st.split(':')[0]
		state_output = st.split(':')[1]
		STATEMACHINE[state_name] = {"next_states" : {}, "output" : state_output}
	
	#Find all transitions
	#raw_transitions = tree.xpath("/mxGraphModel/root/Connector/mxCell[@style='straightConnector']")
	raw_transition_parents = tree.xpath("/mxGraphModel/root/Connector/mxCell[@style='straightConnector']/..")
	
	transitions = []
	for rtp in raw_transition_parents:
		src = rtp.xpath("mxCell/@source")[0]
		tgt = rtp.xpath("mxCell/@target")[0]
		#Get the associated transition signal
		sig = rtp.xpath("@label")[0]
		
		transitions.append((src, tgt, sig))
	
	#print transitions
	
	#Resolve transitions
	for src,dst,sig in transitions:
		#Get source
		res_src = tree.xpath("/mxGraphModel/root/Shape[@id='" + str(src) + "']/@label")[0]
		#Get destination
		res_dst = tree.xpath("/mxGraphModel/root/Shape[@id='" + str(dst) + "']/@label")[0]
		
		
		
		#print str((res_src, res_dst))
		
		res_src_name = res_src.split(':')[0]
		res_dst_name = res_dst.split(':')[0]
		
		#print str((res_src_name, res_dst_name, sig))
		
		#Place the program transitions into STATEMACHINE
		STATEMACHINE[res_src_name]['next_states'][str(sig)] = res_dst_name
		
		
	return [STATEMACHINE, initial_state.split(':')[0]]
	
	
		
	
	
	
