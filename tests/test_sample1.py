from litcore import *
import json
import os
import sys

def exp1():
	markup_table = json.load(open('lmt1.json', 'r'))
	print(markup_table)
	with open('crude/sample1.md', 'r') as fp:
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

exp1()