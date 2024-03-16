import os
import sys
import time

import re
import math

from pathlib import Path

import json


trd = '''{
	"module-startswith": "@",
	"chunk-header-regex": "(^<<)(.+)(>>=\\\\s*$)",
	"chunk-continuation-header-regex": "<<\\\\2>>+=",
	"chunk-ref-regex": "(^\\\\s*<<)(.+?)(>>\\\\s*$)",
	"comment-startswith": "",
	"comment-endswith": "",
	"to-ignore-in-chunk": ["^```.*$"],
	"to-ignore-in-prose": [],
	"hooks": []
}
'''

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

def main():
	global trd
	banner = 'LINIT 0.05 (bootstrap version)'
	print(banner)
	cmd_args = get_cmd_args_dict()
	if not cmd_args:
		print('No command-line argument passed!')
		exit(1)
	elif ('-h' in cmd_args) or ('--help' in cmd_args):
		print(
			'Usage: linit -f [FILES]\n' +
			'Print a dictionary to be used by either ltangle or lweave when parsing WEB file(s)\n' + 
			'Options:\n' + 
			'{0:10}'.format('-f') + 
			'{0:32}'.format('Filename(s) to which the dictionary is to be written\n')
		)
	elif '-f' in cmd_args:
		# Fetch the full path of the file to be written
		fname_list = cmd_args['-f']
		if not fname_list:
			print('Filename(s) have not been provided!')
			exit(1)
		for fname in fname_list:
			print(fname)
			# Check whether file exists or not
			if os.path.isfile(fname):
				print('File already exists. Skipping...')
			# If not, then proceed with writing it
			else:
				# Make the directory
				Path(fname).parent.mkdir(parents = True, exist_ok = True)
				# Write the dictionary to file
				with open(fname, 'w') as fp:
					fp.write(trd)
	else:
		print('No valid command-line argument provided!')
		exit(1)
	print('linit has done its job. Now exiting like a nice boy.')

main()
