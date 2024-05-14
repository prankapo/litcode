import os
import sys

import re

import json

from pathlib import Path

from litcode.litcore import *

lweave_help = '''
Purpose
-------
Tangle a code chunk out of file(s) containing literate programs and write it to the file(s) specified.

Usage
-----
lweave [file(s)] [-lmt literate/markup/table/to/use] [-mmt markup/table/to/use] \\
        [-o output_file(s)]

Example Usage
-------------
* lweave common.txt program1.txt -lmt lmt4c.json -mmt md.json -o Program1.md
* lweave common.txt program1.txt -o Program1.txt 

Notes
-----
1. If no literate markup table is provided, then the default markup table for literate programming defined in
   litcore is used.
2. If no markup table (for a markup language) is specified, then the markup table for plain-text is used. 
3. If -o option is not used, woven output will be printed on the screen. 

Options
-------
-o .......... Name of the file(s) to which the tangled code is to be written
-lmt ........ Markup table containing symbols used for marking elements of a literate program
-mmt ........ Markup table containing symbols of markup language used
-h, --help .. Print brief documentation of lweave
'''

def get_woven_lines(fname_list, literate_markup_table, markup_language_markup_table):
    chunk_name_map = get_chunk_name_map(fname_list, literate_markup_table)
    # print(json.dumps(chunk_name_map, indent = 4))
    chunk_definition_position_map = dict()
    content = ''
    woven_lines = []
    for fname in fname_list:
        with open(fname, 'r') as fp:
            content += ''.join(fp.readlines())
    lexer = LitCodeLexer(content, literate_markup_table)
    lexer.start()
    lexer_state = ''
    char_read_by_lexer = ''
    chunk_definition_name = ''
    module_number = 0
    while lexer_state != 'HALT':
        lexer_result = lexer.read()
        lexer_state = lexer_result[0]
        char_read_by_lexer = lexer_result[1]
        if lexer_state == 'RESET MODULE COUNTER':
            module_number = 0
        elif lexer_state == 'NEW MODULE BEGINS':
            module_number += 1
        elif lexer_state == 'START READING CHUNK DEFINITION NAME':
            chunk_definition_name = ''
        elif lexer_state == 'READING CHUNK DEFINITION NAME':
            chunk_definition_name += get_processed_char_when_reading_chunk_name(
                                                char_read_by_lexer, chunk_definition_name)
        elif lexer_state == 'STOP READING CHUNK DEFINITION NAME':
            chunk_definition_name = chunk_name_map[chunk_definition_name]
            if chunk_definition_name not in chunk_definition_position_map:
                chunk_definition_position_map[chunk_definition_name] = [module_number]
            elif chunk_definition_name in chunk_definition_position_map:
                chunk_definition_position_map[chunk_definition_name].append(module_number)
    '''
    for chunk_definition_name in chunk_definition_position_map:
        locations = ', '.join([str(loc) for loc in chunk_definition_position_map[chunk_definition_name]])
        chunk_definition_position_map[chunk_definition_name] = locations
    '''
    # print(json.dumps(chunk_definition_position_map, indent = 4))
    lexer.reset(content)
    lexer_state = ''
    module_number = 0
    chunk_definition_name = ''
    chunk_reference_name = ''
    insert_code_block_end = False
    while lexer_state != 'HALT':
        lexer_result = lexer.read()
        lexer_state = lexer_result[0]
        char_read_by_lexer = lexer_result[1]
        if lexer_state == 'RESET MODULE COUNTER' or lexer_state == 'NEW MODULE BEGINS':
            if insert_code_block_end is True:
                insert_code_block_end = False
                if len(markup_language_markup_table['code-block-endswith']) != 0:
                    woven_lines += '\n' + markup_language_markup_table['code-block-endswith'] + '\n'
        if lexer_state == 'RESET MODULE COUNTER':
            module_number = 0
        elif lexer_state == 'NEW MODULE BEGINS':
            module_number += 1
            woven_lines += markup_language_markup_table['new-module-startswith']
            woven_lines += str(module_number)
            woven_lines += markup_language_markup_table['new-module-endswith']
        elif lexer_state == 'START READING CHUNK DEFINITION NAME':
            chunk_definition_name = ''
            woven_lines += markup_language_markup_table['chunk-name-startswith']
        elif lexer_state == 'READING CHUNK DEFINITION NAME':
            chunk_definition_name += get_processed_char_when_reading_chunk_name(
                                                char_read_by_lexer, chunk_definition_name)
        elif lexer_state == 'STOP READING CHUNK DEFINITION NAME':
            chunk_definition_name = chunk_name_map[chunk_definition_name]
            locations = chunk_definition_position_map[chunk_definition_name]
            chunk_definition_name_with_loc = chunk_definition_name + ' '
            chunk_definition_name_with_loc += markup_language_markup_table['small-size-startswith']
            chunk_definition_name_with_loc += ', '.join([str(loc) for loc in locations])
            chunk_definition_name_with_loc += markup_language_markup_table['small-size-endswith']
            chunk_definition_name_with_loc += markup_language_markup_table['normal-size-startswith']
            chunk_definition_name_with_loc += markup_language_markup_table['normal-size-endswith']
            woven_lines += chunk_definition_name_with_loc
            if module_number == locations[0]:
                woven_lines += markup_language_markup_table['chunk-name-endswith']
                woven_lines += '\n'
                if len(markup_language_markup_table['code-block-startswith']) != 0:
                    woven_lines += markup_language_markup_table['code-block-startswith'] + '\n'
            elif module_number > locations[0]:
                woven_lines += markup_language_markup_table['chunk\'s-continuation-name-endswith']
                woven_lines += '\n'
                if len(markup_language_markup_table['code-block-startswith']) != 0:
                    woven_lines += markup_language_markup_table['code-block-startswith'] + '\n'
            insert_code_block_end = True
        elif lexer_state == 'START READING CHUNK REFERENCE NAME':
            chunk_reference_name = ''
            if lexer.is_reading_code() is True:
                woven_lines += markup_language_markup_table['incode-chunk-reference-startswith']
            elif lexer.is_reading_code() is False:
                woven_lines += markup_language_markup_table['chunk-reference-startswith']
        elif lexer_state == 'READING CHUNK REFERENCE NAME': 
            chunk_reference_name += get_processed_char_when_reading_chunk_name(
                                                char_read_by_lexer, chunk_reference_name)
        elif lexer_state == 'STOP READING CHUNK REFERENCE NAME':
            chunk_reference_name = chunk_name_map[chunk_reference_name]
            locations = chunk_definition_position_map[chunk_reference_name]
            chunk_reference_name_with_loc = chunk_reference_name + ' '
            chunk_reference_name_with_loc += markup_language_markup_table['small-size-startswith']
            chunk_reference_name_with_loc += ', '.join([str(loc) for loc in locations])
            chunk_reference_name_with_loc += markup_language_markup_table['small-size-endswith']
            chunk_reference_name_with_loc += markup_language_markup_table['normal-size-startswith']
            chunk_reference_name_with_loc += markup_language_markup_table['normal-size-endswith']
            woven_lines += chunk_reference_name_with_loc
            if lexer.is_reading_code() is True:
                woven_lines += markup_language_markup_table['incode-chunk-reference-endswith']
            elif lexer.is_reading_code() is False:
                woven_lines += markup_language_markup_table['chunk-reference-endswith']
        else:
            if lexer.is_escape_sequence_escaped() is True:
                woven_lines.pop(-1)
            woven_lines += char_read_by_lexer
    if insert_code_block_end is True:
        insert_code_block_end = False
        if len(markup_language_markup_table['code-block-endswith']) != 0:
            woven_lines += '\n' + markup_language_markup_table['code-block-endswith'] + '\n'
    woven_lines = ''.join(woven_lines)
    woven_lines = woven_lines.replace(chr(0x00), '')
    return woven_lines

def main():
    global lweave_help, version
    banner = f'LWEAVE {version}'
    print(banner)
    cmd_args = None
    fname_list = []
    ofname_list = []
    debug_mode = False
    # Get dictionary of command-line arguments
    cmd_args = get_cmd_args_dict()
    are_cmd_args_valid = False
    # Process these command-line arguments
    if not cmd_args:
        print('No arguments have been passed!')
        are_cmd_args_valid = False
    elif ('-h' in cmd_args) or ('--help' in cmd_args):
        print(lweave_help)
        are_cmd_args_valid = 0.5
    elif '' in cmd_args:
        # Get file-names
        fname_list = cmd_args['']
        # Check if the fname_list is empty
        if not fname_list:
            print('No filename(s) have been provided!')
            are_cmd_args_valid = False
        else:
            are_cmd_args_valid = True
        if '-trd' in cmd_args:
            trd_fname = cmd_args['-trd'][0]
            trd = json.load(open(trd_fname, 'r'))
        # Load the name of the files to which the woven output is to be written, else
        # print it on the screen
        if '-o' in cmd_args:
            ofname_list = cmd_args['-o']
        if '-o' not in cmd_args or ofname_list == []:
            debug_mode = True
            # print('No output files have been specified!\nWoven output will be printed on the screen.')
        if '-lmt' in cmd_args:
            lmt_fname = cmd_args['-lmt'][0]
            literate_markup_table = json.load(open(f'{lmt_fname}', 'r'))
        else:
            literate_markup_table = get_default_markup_table(markup_name = 'literate', as_string = False)
        if '-mmt' in cmd_args:
            mmt_fname = cmd_args['-mmt'][0]
            markup_language_markup_table = json.load(open(f'{mmt_fname}', 'r'))
        else:
            markup_language_markup_table = get_default_markup_table(markup_name = 'plain-text', 
                                                                    as_string = False)
    if are_cmd_args_valid is not True:
        exit(1)
    # Generate woven lines
    woven_lines = get_woven_lines(fname_list, literate_markup_table, markup_language_markup_table)
    # Write the woven output to the files if debug_mode = False, else print it on the screen
    # woven_lines = ''.join(woven_lines)
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
    print('lweave has done its job.')
