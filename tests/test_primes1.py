from litcore import *
import json
import os
import sys

def exp4():
	markup_table = json.load(open('lmt2.json', 'r'))
	print(markup_table)
	chunk_name_map = get_chunk_name_map(['primes/primes.md'], markup_table)
	print(json.dumps(chunk_name_map, indent = 4))

exp4()