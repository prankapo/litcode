from litcore import *
import json
import os
import sys

def exp3():
	markup_table = json.load(open('lmt2.json', 'r'))
	print(markup_table)
	with open('crude/sample3.txt', 'r') as fp:
		lines = ''.join(fp.readlines())
	lexer = LitCodeLexer(lines, markup_table)
	state = lexer.start()
	print(f'Max escape sequence char size:' \
		f'{lexer.escape_sequence_check_counter_limit}')
	print(f'Printing escape_sequences {lexer.escape_sequences}')
	while(state != 'HALT'):
		lexer_result = lexer.read()
		state = lexer_result[0]
		char = lexer_result[1]
		print(f'Result: .{state}..{char}..{lexer.is_reading_code()}')
	fname_list = ['crude/sample3.txt']
	chunk_name_map = get_chunk_name_map(fname_list, markup_table)
	print(json.dumps(chunk_name_map, indent = 4))

exp3()