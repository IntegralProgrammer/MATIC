#!/usr/bin/env python
# -*- coding: utf-8 -*-

import NODE__enterkey
import NODE__tagger
import NODE__printer
import NODE__gain
import NODE__adder
import NODE__xor
import NODE__fsm
import NODE__hex_to_bytes
import NODE__str_to_hex
import NODE__to_string
import NODE__connected_fsm
import NODE__equality
import NODE__inequality
import NODE__unicorn_nacl_sign
import NODE__unicorn_nacl_verify
import NODE__unicorn_nacl_open
import NODE__unicorn_zlib_deflate
import NODE__unicorn_zlib_inflate

#Map node types to their constructors
types_map = {}
types_map["enterkey"] = NODE__enterkey.NODE__enterkey
types_map["tagger"] = NODE__tagger.NODE__tagger
types_map["printer"] = NODE__printer.NODE__printer
types_map["gain"] = NODE__gain.NODE__gain
types_map["adder"] = NODE__adder.NODE__adder
types_map["xor"] = NODE__xor.NODE__xor
types_map["fsm"] = NODE__fsm.NODE__fsm
types_map["hex_to_bytes"] = NODE__hex_to_bytes.NODE__hex_to_bytes
types_map["str_to_hex"] = NODE__str_to_hex.NODE__str_to_hex
types_map["to_string"] = NODE__to_string.NODE__to_string
types_map["connected_fsm"] = NODE__connected_fsm.NODE__connected_fsm
types_map["equality"] = NODE__equality.NODE__equality
types_map["inequality"] = NODE__inequality.NODE__inequality
types_map["unicorn_nacl_sign"] = NODE__unicorn_nacl_sign.NODE__unicorn_nacl_sign
types_map["unicorn_nacl_verify"] = NODE__unicorn_nacl_verify.NODE__unicorn_nacl_verify
types_map["unicorn_nacl_open"] = NODE__unicorn_nacl_open.NODE__unicorn_nacl_open
types_map["unicorn_zlib_deflate"] = NODE__unicorn_zlib_deflate.NODE__unicorn_zlib_deflate
types_map["unicorn_zlib_inflate"] = NODE__unicorn_zlib_inflate.NODE__unicorn_zlib_inflate

def construct_node(node_type, node_args):
	return types_map[node_type](*node_args)


