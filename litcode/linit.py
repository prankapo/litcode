import os
import sys

import re

import json

from pathlib import Path

from litcode.litcore import *

linit_help = '''
Purpose
-------
Write markup tables to be used by either ltangle or lweave or litcode's extensions when processing file(s) 
containing literate programs.

Usage
-----
linit -markup [markup language] -o [file(s)]

Example Usage
-------------
* `$ linit -o python.json c.json` writes the default literate markup table (similar to Noweb markup) to
  python.json and c.json.
* `$ linit -markup markdown -o doc.json` writes the markup table used for markdown files to doc.json.

Notes
-----
1. If -markup option is not used, the default literate markup table gets written to the specified files.  
2. If a markup table has already been written to the file specified on command-line, the file is not
   rewritten. This avoids accidental overwriting of modifications made to a markup table by the user.  

Options
-------
-o .......... Filename(s) to which the table is to be written
-markup ..... Name of the markup table to be written
              Available options: 
                    * literate:   for reading literate programs, similar to Noweb style.
                    * markdown:   for literate programs written in markdown files
                    * plain-text: for literate programs written in plain-text files
                    * rst:        for literate programs written in restructured text files
                    * tex:        for literate programs written in tex (or latex)
              Literate markup table selected for a project will be used by both ltangle and lweave. 
              Markup tables specific for a markup language (example: markdown or tex) will be used only by
              lweave for pretty printing. 
-h, --help .. Print brief documentation of linit
'''

def main():
    global linit_help, version
    banner = f'LINIT {version}'
    print(banner)
    fname_list = []
    markup_name = 'literate'
    markup_table = dict()
    cmd_args = get_cmd_args_dict()
    are_cmd_args_valid = False
    if not cmd_args:
        print('No arguments have been passed!')
        are_cmd_args_valid = False
    elif ('-h' in cmd_args) or ('--help' in cmd_args):
        print(linit_help)
        are_cmd_args_valid = True
    elif '' in cmd_args:
        if '-o' in cmd_args:
            # Fetch the full path of the file(s) to be written
            fname_list = cmd_args['-o']
            if not fname_list:
                print('Filename(s) have not been provided!')
                are_cmd_args_valid = False
            else:
                are_cmd_args_valid = True
        # It is ok if -markup switch is not specified. Therefore, are_cmd_args_valid is determined only by the
        # presence of -h or -o options. 
        if '-markup' in cmd_args:
            if cmd_args['-markup']:
                markup_name = cmd_args['-markup'][0]
            else:
                markup_name = ''
            if markup_name not in ['literate', 'markdown', 'plain-text', 'rst', 'tex']:
                print(f'{markup_name} is not defined in LitCode.\n'
                        'Writing markup table for plain-text. Modify it as required.')
                markup_name = 'plain-text'
        else:
            print(f'Writing literate markup table...')
    if are_cmd_args_valid is False:
        # print(f'Command-line argument validity failed!\nExiting...')
        exit(1)
    markup_table = get_default_markup_table(markup_name = markup_name, as_string = True)
    for fname in fname_list:
        print(fname)
        # Check whether file exists or not. If it does exists, then don't overwrite its contents.
        if os.path.isfile(fname):
            print('File already exists. Skipping...')
        # If not, then proceed with writing the dictionary/table to it.
        else:
            # Make the directory
            Path(fname).parent.mkdir(parents = True, exist_ok = True)
            # Write the dictionary to file
            with open(fname, 'w') as fp:
                fp.write(markup_table)
    print('linit has done its job.')
