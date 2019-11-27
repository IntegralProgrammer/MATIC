#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import convert_fsm_model


def resolve_type(node_type, node_name):
	if node_type in RESOLVERS:
		return RESOLVERS[node_type](node_name)
	else:
		return []
	

def resolve_fsm(node_name):
	this_dir_contents = os.listdir('.')
	#Find the appropriate XML file
	if node_name + ".xml" in this_dir_contents:
		print "[OK] Found the XML file defining FSM " + node_name
		return convert_fsm_model.convert_xml_fsm(node_name)
	else:
		print "[Error] XML file for FSM " + node_name + " not found."
		return []
	
	
	
RESOLVERS = {}
RESOLVERS['fsm'] = resolve_fsm
