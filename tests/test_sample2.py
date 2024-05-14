from litcore import *
import json
import os
import sys

def exp2():
	markup_table = json.load(open('lmt1.json', 'r'))
	print(markup_table)
	fname_list = ['crude/sample2.txt']
	chunk_name_map = get_chunk_name_map(fname_list, markup_table)
	print(json.dumps(chunk_name_map, indent = 4))

exp2()