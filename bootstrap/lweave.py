import os
import sys
import time

import re
import math

from pathlib import Path

import json


trd = None
woven_lines = None

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

def get_woven_lines(fname_list, trd):
	chunk_name = None
	chunk_name_list = []
	woven_lines = []
	for fname in fname_list:
		lines = None
		reading_chunk = False
		with open(fname, 'r') as fp:
			lines = fp.readlines()
		print(fname)
		for line in lines:
			if trd['to-ignore-in-prose']:
				if re.search(trd['to-ignore-in-prose'], line):
					continue
			tmp_line = line.lstrip(trd['module-startswith'])
			tmp_line = tmp_line.lstrip()
			chunk_name = re.search(trd['chunk-header-regex'], tmp_line)
			if chunk_name:
				print(chunk_name)
				chunk_name = chunk_name.group(2)
				if chunk_name not in chunk_name_list:
					chunk_name_list.append(chunk_name)
				else:
					line = re.sub(trd['chunk-header-regex'], trd['chunk-continuation-header-regex'], line)
					line += '\n'
			woven_lines.append(line)
	return woven_lines

def main():
	global trd, woven_lines
	banner = 'LWEAVE 0.05 (bootstrap version)'
	print(banner)
	cmd_args = None
	fname_list = []
	ofname_list = []
	trd_fname = None
	debug_mode = False
	hook_list = []
	hook_lines = None
	# Get dictionary of command-line arguments
	cmd_args = get_cmd_args_dict()
	# Process these command-line arguments
	if not cmd_args:
		print('No arguments have been passed!')
		exit(1)
	elif ('-h' in cmd_args) or ('--help' in cmd_args):
		print(
			'Usage: lweave [FILES] -trd [FILE[.json]] [OPTIONS]\n' +
			'Weave a beautiful document containing the content of WEB files' + 
			'using a translation dictionary\n' + 
			'Options:\n' + 
			'{0:10}'.format('-trd') + 
			'{0:32}'.format('Name of the translation dictionary to be used while weaving the files.\n') +
			'{0:10}'.format('-hk') + 
			'{0:32}'.format('Name of the hooks to be executed after preprocessing the content of \n') + 
			'{0:10}'.format('') +
			'{0:32}'.format('WEB files. Hooks are executed in the order they are presented\n') +
			'{0:10}'.format('-o') +
			'{0:32}'.format('Files to which the woven prose is to be written.\n')
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
			print('Translation dictionary to be used during weaving has not been specified!\n')
			exit(1)
		# Load the name of the files to which the woven output is to be written, else
		# print it on the screen
		if '-o' in cmd_args:
			ofname_list = cmd_args['-o']
		if '-o' not in cmd_args or ofname_list == []:
			debug_mode = True
			print('No output files have been specified!\nWoven output will be printed on the screen.')
		# Load the names of the hooks that have been provided. If none are specified, then no hooks will be
		# executed by default
		if '-hk' in cmd_args:
			hook_list = cmd_args['-hk']
	else:
		print('No filename(s) have been provided!')
		exit(1)
	# Generate woven lines
	woven_lines = get_woven_lines(fname_list, trd)
	# Execute the hooks
	for hook in hook_list:
		if hook in trd["hooks"]:
			with open(hook, 'r') as fp:
				hook_lines = fp.readlines()
			hook_lines = ''.join(hook_lines)
			print(f'Executing hook: {hook}')
			exec(hook_lines, globals())
	# Write the woven output to the files if debug_mode = False, else print it on the screen
	woven_lines = ''.join(woven_lines)
	if debug_mode:
		print('-' * 110)
		print(f'Woven output')
		print('-' * 110)
		print(woven_lines)
	else:
		for ofname in ofname_list:
			print(f'Attempting to write to {ofname}')
			# Make the directory
			Path(ofname).parent.mkdir(parents = True, exist_ok = True)
			# Write the dictionary to file
			with open(ofname, 'w') as fp:
				fp.write(woven_lines)
			print(f'{ofname} written.')
	print('lweave has done its job. Consider it a gift from God!')

main()