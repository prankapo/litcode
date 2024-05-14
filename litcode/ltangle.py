import os
import sys

import re

import json

from pathlib import Path

from litcode.litcore import *

ltangle_help = '''
Purpose
-------
Tangle a code chunk out of file(s) containing literate programs and write it to the file(s) specified.

Usage
-----
ltangle [file(s)] [-c chunk-name] [-lmt markup/table/to/use] \\
        [-t tab-size] [-remindent indentation-level] \\
        [-o output_file(s)]

Example Usage
-------------
* ltangle common.txt program1.txt -c main.c -lmt lmt4c.json -t 4 -o main.c Archive/V0.34/main.c
* ltangle program1.txt common.txt -o init.c

Notes
-----
1. If no chunk name is specified, the first chunk which is found in the literate programs is extracted.  
2. If no makrup table is specified, the default markup table for literate programming specified in litcore is
   used. 
3. If no output files are specified to which the tangled source code is to be written, ltangle will operate in
   debug mode. In debug mode, the dictionary of chunk definitions and tangled lines are printed on screen.
4. If -t option is not used, tabs used for indentation are replaced by 4 spaces.

Options
-------
-c .......... Name of the code chunk to be tangled
-o .......... Name of the file(s) to which the tangled code is to be written
-lmt ........ Markup table to be used during tangling
-h, --help .. Print brief documentation of ltangle
-t .......... Replace n spaces by tabs
-rind ....... Replace r level(s) of indentation
-rnul ....... Do not include lines containing only whitespace in tangled output
-L .......... Insert line number (in literate program) from which the source line originates as a comment
'''

def get_chunk_definition_dict(fname_list, markup_table, include_comments = False):
    chunk_name_map = get_chunk_name_map(fname_list, markup_table)
    chunk_definition_dict = dict()
    for fname in fname_list:
        line_number = 0
        content = ''
        with open(fname, 'r') as fp:
            content = ''.join(fp.readlines())
        lexer = LitCodeLexer(content, markup_table)
        lexer.start()
        lexer_state = ''
        char_read_by_lexer = ''
        chunk_definition_name = ''
        chunk_reference_name = ''
        code = []
        line = ''
        while lexer_state != 'HALT':
            lexer_result = lexer.read()
            lexer_state = lexer_result[0]
            char_read_by_lexer = lexer_result[1]
            if char_read_by_lexer == '\n':
                line_number += 1
            if lexer.is_reading_code() is False:
                if lexer_state == 'START READING CHUNK DEFINITION NAME':
                    if '@->top level chunk' not in chunk_definition_dict and chunk_definition_dict != {}:
                        chunk_definition_dict['@->top level chunk'] = chunk_definition_name
                    code = ''.join(code)
                    chunk_definition_dict[chunk_definition_name] = code.strip(chr(0))
                    chunk_definition_name = ''
                    code = []
                    line = ''
                elif lexer_state == 'READING CHUNK DEFINITION NAME':
                    char_read_by_lexer = get_processed_char_when_reading_chunk_name(
                                                char_read_by_lexer, chunk_definition_name)
                    chunk_definition_name += char_read_by_lexer
                elif lexer_state == 'STOP READING CHUNK DEFINITION NAME':
                    chunk_definition_name = chunk_name_map[chunk_definition_name]
                    if chunk_definition_name in chunk_definition_dict:
                        code += chunk_definition_dict[chunk_definition_name]
            elif lexer.is_reading_code() is True and lexer_state != 'IGNORE':
                if (lexer_state == 'CODE') and (char_read_by_lexer == '\n') \
                and (include_comments is True) and (len(line.strip()) != 0):
                    pattern = markup_table['chunk-reference-startswith'] + '.*' \
                            + markup_table['chunk-reference-endswith']
                    if re.search(pattern, line) is None:
                        code += ' ' + markup_table['comment-startswith'] + ' ' \
                            + f'line {line_number} in {fname}' + ' ' + markup_table['comment-endswith'] \
                            + char_read_by_lexer
                        line = ''
                    else:
                        code += char_read_by_lexer
                        line = ''
                elif lexer_state == 'START READING CHUNK REFERENCE NAME':
                    chunk_reference_name = ''
                    code += char_read_by_lexer
                    line += char_read_by_lexer
                elif lexer_state == 'READING CHUNK REFERENCE NAME':
                    char_read_by_lexer = get_processed_char_when_reading_chunk_name(
                                                char_read_by_lexer, chunk_reference_name)
                    chunk_reference_name += char_read_by_lexer
                    code += char_read_by_lexer
                    line += char_read_by_lexer
                elif lexer_state == 'STOP READING CHUNK REFERENCE NAME':
                    # chunk_reference_name = chunk_name_map[chunk_reference_name]
                    code += char_read_by_lexer
                    line += char_read_by_lexer
                else:
                    code += char_read_by_lexer
                    line += char_read_by_lexer
        if lexer_state == 'HALT':
            code = ''.join(code)
            chunk_definition_dict[chunk_definition_name] = code.strip(chr(0))
    return chunk_definition_dict

def print_chunk_definition_dict(chunk_definition_dict):
    print('-' * 110)
    print('Printing chunk_definition_dict')
    print('-' * 110)
    print('-' * 110)
    for chunk_name in chunk_definition_dict:
        all_lines = chunk_definition_dict[chunk_name]
        all_lines = ''.join(all_lines)
        print(f'<<{chunk_name}>>=')
        print(all_lines)
        print('-' * 110)

def expand_chunk_name(chunk_name, markup_table, chunk_definition_dict):
    # Just check before-hand whether chunk_name exists or not
    if chunk_name in chunk_definition_dict: 
        code = chunk_definition_dict[chunk_name]
    else: 
        print(f'FATAL ERROR! {chunk_name} is not defined in the file(s) passed as command-line arguments!\a')
        exit(1)
    lexer = LitCodeLexer(code, markup_table)
    lexer.start()
    lexer_state = ''
    char_read_by_lexer = ''
    chunk_reference_name = ''
    code = []
    line = ''
    indentation = ''
    while lexer_state != 'HALT':
        lexer_result = lexer.read()
        lexer_state = lexer_result[0]
        char_read_by_lexer = lexer_result[1]
        if lexer_state == 'START READING CHUNK REFERENCE NAME':
            indentation = ' ' * len(line)
        elif lexer_state == 'READING CHUNK REFERENCE NAME':
            chunk_reference_name += get_processed_char_when_reading_chunk_name(
                                            char_read_by_lexer, chunk_reference_name)
        elif lexer_state == 'STOP READING CHUNK REFERENCE NAME':
            definition_of_chunk_reference_name = ''.join(
                                                    expand_chunk_name(
                                                        chunk_reference_name, 
                                                        markup_table,
                                                        chunk_definition_dict
                                                            )
                                                        )
            chunk_reference_name = ''
            definition_of_chunk_reference_name = definition_of_chunk_reference_name.replace('\n',
                                                    '\n' + indentation)
            code += definition_of_chunk_reference_name
        elif lexer_state != 'IGNORE':
            if lexer.is_escape_sequence_escaped() is True:
                # print(f'*** Dealing with escape sequences {char_read_by_lexer}')
                code.pop(-1)
            code += char_read_by_lexer
            if char_read_by_lexer == '\n':
                line = ''
            else:
                line += char_read_by_lexer
    tangled_lines = []
    for line in ''.join(code).split('\n'):
        tangled_lines.append(line + '\n')
    return tangled_lines

def indentation_handler(tangled_lines, use_tabs, tab_size, 
                        levels_of_indentations_to_remove, remove_empty_lines):
    buffer = []
    for line in tangled_lines:
        if use_tabs is True:
            line = line.replace(' ' * tab_size, '\t')
        else:
            line = line.replace('\t', ' ' * tab_size)
        # Remove indentation
        if levels_of_indentations_to_remove > 0:
            indentation = re.findall(r'^(\s*).*$', line)[0]
            if use_tabs is True:
                indentation = indentation[levels_of_indentations_to_remove:]
            else:
                indentation = indentation[levels_of_indentations_to_remove * tab_size:]
            line = indentation + line.lstrip()
        # Remove empty lines
        if remove_empty_lines is True:
            if len(line.strip()) > 0:
                buffer.append(line)
        else:
            buffer.append(line)
    tangled_lines = buffer
    return tangled_lines

def main():
    global ltangle_help, version
    banner = 'LTANGLE ' + version
    print(banner)
    # Setting default values of variables
    fname_list = []
    ofname_list = None
    markup_table_fname = None
    chunk_name = None
    debug_mode = False
    include_comments = False
    use_tabs = False
    tab_size = 4
    levels_of_indentations_to_remove = 0
    remove_empty_lines = False
    tangled_lines = None
    buffer = None
    # Get command-line args as a dictionary
    cmd_args = get_cmd_args_dict()
    are_cmd_args_valid = False
    # Validate the command-line arguments that have been passed.
    # Ascertain whether any arguments have been passed or not
    if not cmd_args:
        print('No arguments have been passed!')
        are_cmd_args_valid = False
    # It the user wishes to get some help, then he shall have it and nothing more!
    elif ('-h' in cmd_args) or ('--help' in cmd_args):
        print(ltangle_help)
        are_cmd_args_valid = 0.5        # Commad-line args are valid. Just print brief documentation
    elif '' in cmd_args:
        # Get file-names
        fname_list = cmd_args['']
        # Check if the fname_list is empty
        if not fname_list:
            print('No filename(s) have been provided!')
            are_cmd_args_valid = False
        else:
            are_cmd_args_valid = True
        # Load the markup table, else throw an error if it has not be provided
        if '-lmt' in cmd_args:
            markup_table_fname = cmd_args['-lmt'][0]
            markup_table = json.load(open(markup_table_fname, 'r'))
        else:
            # print('Markup table to be used during tangling has not been specified!\n')
            # print('Using default markup table for literate programming...')
            markup_table = get_default_markup_table(markup_name = 'literate', as_string = False)
        # See if the chunk_name to be expanded is provided or not. Else work in notebook mode. 
        if '-c' in cmd_args:
            chunk_name = cmd_args['-c']
            if chunk_name:
                chunk_name = chunk_name[0]
            else:
                chunk_name = '*'
        else:
            chunk_name = '*'
        # if chunk_name == '*':
            # print('No chunk name has been provided. ltangle will expand the first chunk it encounters.')
        # Load the name of the files to which the tangled output is to be written, else enter debugging mode
        # and print the markup table and tangled output on the screen
        if '-o' in cmd_args:
            ofname_list = cmd_args['-o']
        if '-o' not in cmd_args or ofname_list == []:
            debug_mode = True
            # print('No output files have been specified!\nTangled output will be printed on the screen.')
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
                # print('Tab-size not provided! 4 will be used.')
                tab_size = 4
        if '-rind' in cmd_args:
            if cmd_args['-rind']:
                levels_of_indentations_to_remove = int(cmd_args['-rind'][0])
                if levels_of_indentations_to_remove <= 0:
                    levels_of_indentations_to_remove = 0
        if '-rnul' in cmd_args:
            remove_empty_lines = True
    if are_cmd_args_valid is not True:
        exit(1)
    # Get a dictionary of chunk definitions
    chunk_definition_dict = get_chunk_definition_dict(fname_list, 
                                                        markup_table, include_comments = include_comments)
    # If no chunk name has been provided, get top_level_chunk_name from chunk_definition_dict
    if chunk_name == '*':
        chunk_name = chunk_definition_dict['@->top level chunk']
    # Get the tangled output.
    # print(f'Calling expand_chunk_name to expand \'{chunk_name}\'')
    tangled_lines = expand_chunk_name(chunk_name, markup_table, chunk_definition_dict)
    
    # tangled_lines = src_line_identifier_handler(tangled_lines, markup_table, include_comments)
    # Convert tabs to spaces or vice-versa, as required. 
    tangled_lines = indentation_handler(tangled_lines, 
                                        use_tabs, tab_size, 
                                        levels_of_indentations_to_remove, 
                                        remove_empty_lines)
    # Time to print the tangled output
    tangled_lines = ''.join(tangled_lines)
    tangled_lines = tangled_lines.replace(chr(0), '')
    if debug_mode:
        print('-' * 110)
        print(json.dumps(markup_table, indent = 4))
        print('-' * 110)
        print_chunk_definition_dict(chunk_definition_dict)
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
    print('ltangle has done its job.')
