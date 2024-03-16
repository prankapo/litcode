import os
import sys
import time

import re
import math

from pathlib import Path

import json


def get_cmd_args_dict():
	cmd_args_list = sys.argv[1:]
	cmd_args_dict = dict()
	switch_name = ''
	values = []
	for cmd_arg in cmd_args_list:
		if cmd_arg.startswith('-'):
			cmd_args_dict[switch_name] = values
			switch_name, values = '', []
			switch_name = cmd_arg
		else:
			values.append(cmd_arg)
		cmd_args_dict[switch_name] = values
	return cmd_args_dict

def get_chunk_dict(fname_list, trd):
	# Initialize the chunk dictionary
	chunk_dict = dict()
	for fname in fname_list:
		# Initialize variables
		lno = 0
		chunk_name = None
		chunk_lines = []
		all_lines = None
		reading_chunk = False
		ignore_chunk_line = False
		# Read all lines from the file
		with open(fname, 'r') as fp:
			all_lines = fp.readlines()
		# Start analyzing the lines one by one.
		for line in all_lines:
			# Increment the line number
			lno += 1
			if reading_chunk:
				if line.startswith(trd['module-startswith']):
					reading_chunk = False
					if chunk_name is not None:
						if '@->top_level_chunk_name' not in chunk_dict:
							chunk_dict['@->top_level_chunk_name'] = chunk_name
						chunk_dict[chunk_name] = chunk_lines
						chunk_name = None
						chunk_lines = []
				else:
					for pattern in trd['to-ignore-in-chunk']:
						if re.search(pattern, line):
							ignore_chunk_line = True
							break
						else:
							ignore_chunk_line = False
					if not ignore_chunk_line:
						indentation = re.search(r'(^[\t\ ]*)(?=\S.*$)', line)
						if indentation: indentation = indentation.group(0)
						else: indentation = ''
						comment_to_refer_src_lno = indentation + f'@->{lno}. in {fname}\n'
						chunk_lines.append(comment_to_refer_src_lno)
						chunk_lines.append(line)
			if not reading_chunk:
				tmp_line = line.lstrip(trd['module-startswith'])
				tmp_line = tmp_line.lstrip()
				chunk_name = re.search(trd['chunk-header-regex'], tmp_line)
				if chunk_name:
					print(chunk_name)
					reading_chunk = True
					chunk_name = chunk_name.group(2)
					if chunk_name in chunk_dict:
						chunk_lines = chunk_dict[chunk_name]
				else:
					reading_chunk = False	# Redundant
		# If you reach EOF while reading a chunk, commit it
		if chunk_name is not None:
			chunk_dict[chunk_name] = chunk_lines
	return chunk_dict

def print_chunk_dict(chunk_dict):	
	print('-' * 110)
	print('Printing chunk_dict')
	print('-' * 110)
	print('-' * 110)
	for chunk_name in chunk_dict:
		all_lines = chunk_dict[chunk_name]
		all_lines = ''.join(all_lines)
		print(f'<<{chunk_name}>>=')
		print(all_lines)
		print('-' * 110)

def get_top_level_chunk_name(fname_list, trd):
	chunk_name = None
	found_chunk = False
	for fname in fname_list:
		all_lines = None
		with open(fname, 'r') as fp:
			all_lines = fp.readlines()
		for line in all_lines:
			if re.search(trd['chunk-header-regex'], line.lstrip(trd['module-startswith'])):
				chunk_name = re.search(trd['chunk-header-regex'], \
							line.lstrip(trd['module-startswith'])).group(2)
				found_chunk = True
				break
		if found_chunk:
			break
		else:
			continue
	return chunk_name

def expand_chunk_name(chunk_name, trd, chunk_dict):
	tangled_lines = []
	# Just check before-hand whether chunk_name exists or not
	if chunk_name in chunk_dict: chunk_lines = chunk_dict[chunk_name]
	else: 
		print(f'FATAL ERROR! {chunk_name} is not defined in the file(s) passed as command-line arguments!\a')
		exit(1)
	for line in chunk_lines:
		# Store the indentation
		indentation = re.search(r'(^[\t\ ]*)(?=\S.*$)', line)
		if indentation: indentation = indentation.group(0)
		else: indentation = ''
		# if you encounter a line matching the chunk-ref-regex, then extract the reference->chunk_name, 
		# and call expand_chunk_name again. 
		chunk_name = re.search(trd['chunk-ref-regex'], line.strip())
		if chunk_name:
			chunk_name = chunk_name.group(2)
			reference_expansion = expand_chunk_name(chunk_name, trd, chunk_dict)
			# Process reference_expansion by adding the indentation of parent to it, and add it to the tangled
			# output 
			tangled_lines += [indentation + child_line for child_line in reference_expansion]
		else:
			tangled_lines.append(line)
	return tangled_lines

def src_line_identifier_handler(tangled_lines, trd, include_comments):
	buffer = []
	for line in tangled_lines:
		tmp_line = line.lstrip()
		if tmp_line.startswith('@->') and include_comments is True:
			line = line.replace('@->', trd['comment-startswith'] + ' ')
			line = line.replace('\n', ' ' + trd['comment-endswith'] + '\n')
		elif tmp_line.startswith('@->') and include_comments is False:
			continue
		buffer.append(line)
	tangled_lines = buffer
	return tangled_lines

def indentation_handler(tangled_lines, use_tabs, tab_size):
	buffer = []
	for line in tangled_lines:
		if use_tabs:
			line = line.replace(' ' * tab_size, '\t')
		else:
			line = line.replace('\t', ' ' * tab_size)
		buffer.append(line)
	tangled_lines = buffer
	return tangled_lines

def main():
	banner = 'LTANGLE 0.05 (bootstrap version)'
	print(banner)
	cmd_args = get_cmd_args_dict()
	fname_list = []
	ofname_list = None
	trd_fname = None
	trd = None
	chunk_name = None
	debug_mode = False
	include_comments = False
	use_tabs = False
	tab_size = 4
	tangled_lines = None
	buffer = None
	# Validate the command-line arguments that have been passed.
	# Ascertain whether any arguments have been passed or not
	if not cmd_args:
		print('No arguments have been passed!')
		exit(1)
	# It the user wishes to get some help, then he shall have it and nothing more!
	elif ('-h' in cmd_args) or ('--help' in cmd_args):
		print(
			'Usage: ltangle [FILES] -trd [FILE[.json]] [OPTIONS]\n' +
			'Extract a chunk from the WEB files using a translation dictionary\n' + 
			'Options:\n' + 
			'{0:10}'.format('-trd') + 
			'{0:32}'.format('Name of the translation dictionary to be used while tangling the file\n') +
			'{0:10}'.format('-c') + 
			'{0:32}'.format('Name of the chunk to be expanded. If not provided, contents of the first \n') +
			'{0:10}'.format('') + 
			'{0:32}'.format('chunk encountered are expanded.\n') +
			'{0:10}'.format('-o') + 
			'{0:32}'.format('Files to which the tangled source code is to be written. If none are \n') +
			'{0:10}'.format('') + 
			'{0:32}'.format('provided then ltangle will print the tangled code on the screen.\n') +
			'{0:10}'.format('-L') +
			'{0:32}'.format('Add line numbers as comments in the tangled code identifying the source\n') +
			'{0:10}'.format('') + 
			'{0:32}'.format('of the line following it.') +
			'{0:10}'.format('\n-t') +
			'{0:32}'.format('Use tabs for indentations; n spaces are converted to tabs. By default, \n') + 
			'{0:10}'.format('') +
			'{0:32}'.format('spaces are used for indentation. If n is not provided, it is set to 4.\n')
		)
		exit(0)
	elif '' in cmd_args:
		# Get file-names
		fname_list = cmd_args['']
		# Check if the fname_list is empty
		if not fname_list:
			print('No filename(s) have been provided!')
			exit(1)
		# Load the translation dictionary, else throw an error if it has not be provided
		if '-trd' in cmd_args:
			trd_fname = cmd_args['-trd'][0]
			trd = json.load(open(trd_fname, 'r'))
		else:
			print('Translation dictionary to be used during tangling has not been specified!\n')
			exit(1)
		# See if the chunk_name to be expanded is provided or not. Else work in notebook mode. 
		if '-c' in cmd_args:
			chunk_name = cmd_args['-c']
			if chunk_name:
				chunk_name = chunk_name[0]
			else:
				chunk_name = '*'
		else:
			chunk_name = '*'
		if chunk_name == '*':
			print('No chunk name has been provided. ltangle will expand the first chunk it encounters.')
		# Load the name of the files to which the tangled output is to be written, else enter debugging mode
		# and print the translation dictionary and tangled output on the screen
		if '-o' in cmd_args:
			ofname_list = cmd_args['-o']
		if '-o' not in cmd_args or ofname_list == []:
			debug_mode = True
			print('No output files have been specified!\nTangled output will be printed on the screen.')
		else:
			debug_mode = False
		# Of course this means that you can `hack' ltangle by running it with -R *
		# Set include_comments = True if -L option is passed
		if '-L' in cmd_args:
			include_comments = True
		# Set use_tabs to True if -t option is passed. By default, 4 spaces = 1 Tab 
		if '-t' in cmd_args:
			use_tabs = True
			if cmd_args['-t']:
				tab_size = int(cmd_args['-t'][0])
			else:
				print('Tabsize not provided! 4 will be used.')
				tab_size = 4
	else:
		print('No filename(s) have been provided!')
		exit(1)
	# Command-line arguments have been parsed. We no longer need to be in darkness of infinite nesting
	# Get a dictionary of chunks.
	chunk_dict = get_chunk_dict(fname_list, trd)
	# If no chunk name has been provided, get top_level_chunk_name from chunk_dict
	if chunk_name == '*':
		chunk_name = chunk_dict['@->top_level_chunk_name']
	# Get the tangled output. This can be done with the help of a recursive function
	print(f'Calling expand_chunk_name to expand \'{chunk_name}\'')
	tangled_lines = expand_chunk_name(chunk_name, trd, chunk_dict)
	# Properly format comment lines using translation dictionary
	tangled_lines = src_line_identifier_handler(tangled_lines, trd, include_comments)
	# Convert tabs to spaces or vice-versa, as required. 
	tangled_lines = indentation_handler(tangled_lines, use_tabs, tab_size)
	# Time to print the tangled output
	tangled_lines = ''.join(tangled_lines)
	if debug_mode:
		print_chunk_dict(chunk_dict)
		print('-' * 110)
		print(f'Expansion of {chunk_name}')
		print('-' * 110)
		print(tangled_lines)
	else:
		for ofname in ofname_list:
			print(f'Attempting to write to {ofname}')
			# Make the directory
			Path(ofname).parent.mkdir(parents = True, exist_ok = True)
			# Write the dictionary to file
			with open(ofname, 'w') as fp:
				fp.write(tangled_lines)
			print(f'{ofname} written.')
	print('ltangle has done its job. Now going away like a good girl.')

main()