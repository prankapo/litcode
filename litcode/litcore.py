import os
import sys

import re

import json

from pathlib import Path

version = '0.10'

default_literate_markup_table = {
    "chunk-name-startswith": "<<",
    "chunk-name-endswith": ">>=",
    "chunk's-continuation-name-endswith": ">>+=",
    "chunk-reference-startswith": "<<",
    "chunk-reference-endswith": ">>",
    "to-ignore-in-chunk-startswith": "```",
    "to-ignore-in-chunk-endswith": "",
    "new-module-startswith": "@",
    "module-counter-reset": "@reset",
    "comment-startswith": "/*",
    "comment-endswith": "*/"
}

markdown_markup_table = {
    "chunk-name-startswith": "&lt;*",
    "chunk-name-endswith": "*&gt;=",
    "chunk's-continuation-name-endswith": "*&gt;+=",
    "code-block-startswith": "",
    "code-block-endswith": "",
    "chunk-reference-startswith": "&lt;",
    "chunk-reference-endswith": "&gt;",
    "incode-chunk-reference-startswith": "/* Insert chunk: <",
    "incode-chunk-reference-endswith": "> */",
    "normal-size-startswith": "",
    "normal-size-endswith": "",
    "small-size-startswith": "<sup><sub>",
    "small-size-endswith": "</sub></sup>",
    "new-module-startswith": "**",
    "new-module-endswith": ".**&nbsp;&nbsp;&nbsp;&nbsp;"
}

plain_text_markup_table = {
    "chunk-name-startswith": "<<",
    "chunk-name-endswith": ">>=",
    "chunk's-continuation-name-endswith": ">>+=",
    "code-block-startswith": "",
    "code-block-endswith": "",
    "chunk-reference-startswith": "<<",
    "chunk-reference-endswith": ">>",
    "incode-chunk-reference-startswith": "<<",
    "incode-chunk-reference-endswith": ">>",
    "normal-size-startswith": "",
    "normal-size-endswith": "",
    "small-size-startswith": "; ",
    "small-size-endswith": "",
    "new-module-startswith": "[",
    "new-module-endswith": "]:    "
}

rst_markup_table = {
    "chunk-name-startswith": ":math:`\\langle` ",
    "chunk-name-endswith": ":math:`\\rangle\\equiv`",
    "chunk's-continuation-name-endswith": ":math:`\\rangle +\\equiv`",
    "code-block-startswith": "",
    "code-block-endswith": "",
    "chunk-reference-startswith": ":math:`\\langle` ",
    "chunk-reference-endswith": ":math:`\\rangle`",
    "incode-chunk-reference-startswith": "/* Insert chunk: <",
    "incode-chunk-reference-endswith": "> */",
    "normal-size-startswith": "",
    "normal-size-endswith": "",
    "small-size-startswith": "",
    "small-size-endswith": "",
    "new-module-startswith": "**",
    "new-module-endswith": ".**    "
}

tex_markup_table = {
    "chunk-name-startswith": "\\par\\noindent\n$\\langle$",
    "chunk-name-endswith": "$\\rangle\\equiv$\\vspace{-10pt}",
    "chunk's-continuation-name-endswith": "$\\rangle +\\equiv$\\vspace{-10pt}",
    "code-block-startswith": "\n\\begin{lstlisting}[upquote=true,"
    "columns=fullflexible,basicstyle=\\fontfamily{SourceCodePro-TLF}\\small,"
    "escapeinside={@<}{@>},language=C]",
    "code-block-endswith": "\\end{lstlisting}",
    "chunk-reference-startswith": "$\\langle$",
    "chunk-reference-endswith": "$\\rangle",
    "incode-chunk-reference-startswith": "@<$\\langle$",
    "incode-chunk-reference-endswith": "$\\rangle$@>",
    "normal-size-startswith": "\\normalsize ",
    "normal-size-endswith": " ",
    "small-size-startswith": "\\footnotesize ",
    "small-size-endswith": " ",
    "new-module-startswith": "\\textbf{",
    "new-module-endswith": ".}~~~~"
}

# get_default_markup_table()
# Return a markup table as either a Python dictionary or a string depending upon the value of the argument
# as_string. Markup table to be returned is specified by the positional parameter markup_name.
def get_default_markup_table(markup_name = 'literate', as_string = False):
    global default_literate_markup_table, \
            markdown_markup_table, plain_text_markup_table, \
            rst_markup_table, tex_markup_table
    markup_table = None
    if markup_name == 'literate':
        markup_table = default_literate_markup_table
    elif markup_name == 'markdown':
        markup_table = markdown_markup_table
    elif markup_name == 'plain-text':
        markup_table = plain_text_markup_table
    elif markup_name == 'rst':
        markup_table = rst_markup_table
    elif markup_name == 'tex':
        markup_table = tex_markup_table
    if as_string is False:
        return markup_table
    elif as_string is True:
        return json.dumps(markup_table, indent = 4)
    else:
        return dict()

# LitCodeLexer: A class whose object can be thought of as an automata which is reading the characters in a
# string. For each character read, it also sets the context in which the character should be read. Both the
# context and the character are returned packed inside a tuple. Context is determined by reading the string
# character by character, matching them to values of keys in a markup table, and then analyzing the current
# and previous state of the lexer. The markup table used by an object of LitCodeLexer is that of a literate
# program: it contains symbols using which chunk names, references, etc. are marked to distinguish code and
# prose.  
class LitCodeLexer():
    def __init__(self, string, markup_table):
        self.previous_state = 'UNDEFINED'
        self.state = 'PROSE'
        self.previous_char = ''
        self.char = ''
        # Append chr(0x00) to the string. These prevents any errors in case the string index overshoots its
        # maximum value. Check while loop in read() method below.  
        self.string = string + chr(0x00)
        self.string_index = 0
        self.max_string_index = len(string) - 1
        self.markup_table = markup_table
        # It might happen that two escape sequences in the markup table are almost similar; they differ only
        # by the last few characters. An example of this would be the Noweb markup style, in which a chunk
        # definition's name and reference name both start with <<.  If were to just match the character read
        # sequentially with the entries in the table, we will most likely end up interpreting the escape
        # sequence partially and incorrectly.  
        # To interpret the escape sequence properly, if we see that the character we have read matches with
        # the first character of any sequence in the table, we can read the next character in the string,
        # concatentate it with character previously and compare to the sequence in the table again. We keep on
        # doing this repeatedly till we do not match any sequence in the table, and then take the last
        # sequence we matched to be the escape sequence. Think of this like a window which keeps on expanding
        # from its right horizontal edge...  
        self.escape_sequence_check_counter_limit = 0
        self.escape_sequence_chars = set()
        self.escape_sequences = set(self.markup_table.values())
        self.concatenated_escape_sequences = ''.join(self.escape_sequences)
        for escape_sequence_name in self.markup_table:
            self.escape_sequence_check_counter_limit = \
                max(self.escape_sequence_check_counter_limit, len(self.markup_table[escape_sequence_name]))
            if len(self.markup_table[escape_sequence_name]) > 0:
                self.escape_sequence_chars.add(\
                    self.markup_table[escape_sequence_name].strip()[0])
        # Set to false if reading prose, else set it to true.  
        self.reading_code = False
        # This variable is set to True if we are using Noweb style markup, where both the chunk definition
        # name and chunk reference name start with same escape sequence and the expanding window algorithm
        # described above won't be helpful.  
        self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq = False
        if self.markup_table['chunk-name-startswith'] == self.markup_table['chunk-reference-startswith']:
            # print('****THERE WILL BE A CLASH!!*******')
            self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq = True
        # Escape sequences defined in literate markup table can also be expanded using a backslash.   
        # For example: std::cout \<< "Hello world" \<< std::endl;   
        self.escape_sequence_escaped = False
    def start(self):
        if self.string_index == 0 and self.state == 'HALT':
            self.state = 'PROSE'
            return self.string_index
        elif self.string_index > 0 and self.state != 'HALT':
            # print(f'Lexer has already been started!'\
            # f'string_index at {self.string_index}')
            return 1
    def reset(self, string):
        self.previous_state = 'UNDEFINED'
        self.state = 'PROSE'
        self.char = ''
        self.string = string + chr(0x00)
        self.string_index = 0
        self.max_string_index = len(self.string) - 1
    def read(self):
        lexer_result = (None, None)
        self.escape_sequence_escaped = False
        if (self.string_index <= self.max_string_index):
            self.previous_char = self.char
            self.char = self.string[self.string_index]
            # print(f'Reading: {self.string_index}: .{self.char}.')
        elif (self.string_index > self.max_string_index):
            self.state = 'HALT'
            self.char = ''
        if self.char in self.escape_sequence_chars and self.state != 'ESCAPE SEQUENCE':
            self.state = 'ESCAPE SEQUENCE'
        if self.state == 'ESCAPE SEQUENCE':
            self.escape_sequence_check_counter = 0
            str_for_storing_escape_sequence = ''
            # Don't tamper with self.string_index when checking if an escape sequence exists or not.  
            escape_sequence_starting_index = self.string_index
            escape_sequence_ending_index = self.string_index
            str_was_matching_with_an_escape_sequence = False
            # Expanding window algorithm for properly detecting an escape sequence/markup symbol is defined
            # here  
            while self.escape_sequence_check_counter <= self.escape_sequence_check_counter_limit:
                # print(f'{self.escape_sequence_check_counter}/{self.escape_sequence_check_counter_limit}')
                # print(f'{escape_sequence_ending_index}/{self.max_string_index}')
                # What would happen if we are reading an escape sequence near the end of a file? We won't be
                # able to detect it. Our whole logic of detecting an escape sequence is based around reading
                # characters till they stop matching any escape sequence in the markup table. To deal with
                # such boundary condition, we have added char 0x00 (NULL) to the end of the string during
                # object initialization so that the escape sequence gets evaluated properly.  
                # Check the constructor.  
                str_for_storing_escape_sequence += self.string[escape_sequence_ending_index]
                # print(f'{str_for_storing_escape_sequence}'
                # f'{str_for_storing_escape_sequence in self.concatenated_escape_sequences}')
                str_matches_with_an_escape_sequence = False
                for escape_sequence in self.escape_sequences:
                    # We are checking length of escape_sequence as those with 0 length will match any string. 
                    # In other words, as an example, '' == 'foo' evaluates to True.  
                    if len(escape_sequence):
                        # If the first char of the string made up of chars till now matches with the first
                        # char of an escape sequence AND this string is a part of escape sequence: then even
                        # if it is a partial match only, we will assume that the escape sequence is present.  
                        if str_for_storing_escape_sequence[0] == escape_sequence[0] \
                            and str_for_storing_escape_sequence in escape_sequence:
                            str_matches_with_an_escape_sequence = True
                            break
                # We will now remember that the string we are concatenating to ONCE used to match an escape
                # sequence. 
                if str_matches_with_an_escape_sequence is True:
                    str_was_matching_with_an_escape_sequence = True
                # If the string is no longer matching any escape sequence, then:
                #   A. We are either having a proper escape sequence
                #   B. We are not having a proper escape sequence. We just the first few chars.
                # We will slice the string to exclude the character we just read, and compare the slice with
                # the escape sequences in the markup table and set up a state accordingly.  
                # If no proper match is there, self.state = 'ESCAPE SEQUENCE', which means that there was no
                # escape sequence to begin with. 
                elif str_matches_with_an_escape_sequence is False \
                    and str_was_matching_with_an_escape_sequence is True:
                    self.char = self.string[escape_sequence_starting_index:escape_sequence_ending_index]
                    for escape_sequence_name in self.markup_table:
                        if self.markup_table[escape_sequence_name] == str_for_storing_escape_sequence[0:-1]:
                            self.state = escape_sequence_name
                            self.char = str_for_storing_escape_sequence[0:-1]
                            # print(f'During match phase: Escape sequences starts at:'
                            # f'{escape_sequence_starting_index}, {escape_sequence_ending_index}')
                            break
                    break
                # counter and index are updated in the end
                self.escape_sequence_check_counter += 1
                escape_sequence_ending_index += 1
            # The sequence of characters we have just read will be returned by the lexer. We need to properly
            # set self.string_index so that they are not re-read again. 
            if str_was_matching_with_an_escape_sequence:
                self.string_index = escape_sequence_ending_index - 1
            # This statement won't be getting executed... Still I am keeping it.@If it works, don't change. 
            else:
                self.string_index = escape_sequence_starting_index
        # print(f'Before returning: .string[{self.string_index}]..{self.string[self.string_index]}.')
        self.string_index += 1
        # ************** [Fixing states] ************
        # 1. Set state if an escape sequence is encountered
        # 2. Set state if chunk definition name and chunk reference name both start with the same escape
        #    sequence. 
        # 3. If state is ESCAPE SEQUENCE, set state = previous_state
        #    Else if state != previous_state, then set previous_state = state
        #    Else if state == previous_state, then determine what we are reading. 
        # Using get method to get the value of key. Indexing operator will return a key error if a key is not
        # there. get() method returns None in that scenario and the program does not terminate.
        if self.char == self.markup_table.get(self.state):
            # If you want to use an escsape sequence defined in the markup table in a weird way, it is
            # recommended that you escape it using a single backward slash.
            if self.previous_char == '\\':
                self.state = self.previous_state
                self.escape_sequence_escaped = True
            if self.state == 'chunk-name-startswith':
                # The following conditional logic has been implemented to ensure that any occurrence of << is
                # not considered as a new chunk defintion. Chunk definitions should strictly begin from a
                # newline or just after a new module declaration, e.g. @ <<Foo.txt>>=
                if (self.string[self.string_index - 5:self.string_index - 3]
                    == (self.markup_table['new-module-startswith'] + ' ')) \
                    or self.previous_char == '\n':
                    self.state = 'START READING CHUNK DEFINITION NAME'
                elif (self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq is True):
                    self.state = 'START READING CHUNK REFERENCE NAME'
                else:
                    self.state = self.previous_state
            elif self.state == 'chunk-name-endswith':
                # The following conditional statements ensure that just using >>= does not mark the end of a
                # chunk's definition name
                if self.previous_state == 'READING CHUNK DEFINITION NAME' \
                    or self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq is True:
                    self.state = 'STOP READING CHUNK DEFINITION NAME'
                    # self.reading_code = True
                else:
                    self.state = self.previous_state
            elif self.state == 'chunk\'s-continuation-name-endswith':
                if self.previous_state == 'READING CHUNK DEFINITION NAME' \
                    or self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq is True:
                    self.state = 'STOP READING CHUNK DEFINITION EXTENSION NAME'
                    # self.reading_code = True
                else:
                    self.state = self.previous_state
                # self.state = 'STOP READING CHUNK DEFINITION EXTENSION NAME'
            elif self.state == 'chunk-reference-startswith':
                self.state = 'START READING CHUNK REFERENCE NAME'
            elif self.state == 'chunk-reference-endswith':
                if self.previous_state == 'READING CHUNK REFERENCE NAME' \
                    or self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq is True:
                    self.state = 'STOP READING CHUNK REFERENCE NAME'
                else:
                    self.state = self.previous_state
            elif self.state == 'to-ignore-in-chunk-startswith':
                self.state = 'IGNORE'
            elif self.state == 'to-ignore-in-chunk-endswith':
                self.state = 'IGNORE'
            elif self.state == 'new-module-startswith':
                # The following logic is implemented to ensure that the string with which a new-module starts
                # should be considered as the beginning of a new module ONLY if it is preceeded by a new-line
                # character and succeeded by a space.  
                if (self.previous_char == '\n' and self.string[self.string_index] == ' ') \
                    or (self.string_index - 1 == 0 and self.string[self.string_index] == ' '):
                    self.state = 'NEW MODULE BEGINS'
                    self.reading_code = False
                else:
                    self.state = self.previous_state
            elif self.state == 'module-counter-reset':
                self.state = 'RESET MODULE COUNTER'
                self.reading_code = False
            elif self.state == 'comment-startswith':
                self.state = 'COMMENT STARTS'
            elif self.state == 'comment-endswith':
                self.state = 'COMMENT ENDS'
        # The following logic is implemented to allow the use of Noweb style of markup where both
        # chunk-definition name and chunk-reference name startswith the same character, namely, <<
        if (self.state == 'START READING CHUNK DEFINITION NAME' 
            or self.state == 'START READING CHUNK REFERENCE NAME') \
            and (self.are_chunk_def_name_and_chunk_ref_name_starting_with_same_esc_seq is True):
            # print('NOWEB STYLE CLASH!!')
            lookahead_lexer = LitCodeLexer(self.string[self.string_index:], self.markup_table)
            lookahead_lexer.start()
            lookahead_lexer_state = self.state
            char_read_by_lookahead_lexer = ''
            while (lookahead_lexer_state not in ('STOP READING CHUNK DEFINITION NAME', 
                    'STOP READING CHUNK DEFINITION EXTENSION NAME',
                    'STOP READING CHUNK REFERENCE NAME')):
                lookahead_lexer_result = lookahead_lexer.read()
                lookahead_lexer_state = lookahead_lexer_result[0]
                char_read_by_lookahead_lexer = lookahead_lexer_result[1]
                # print(f'NOWEB STYLE CLASH.{lookahead_lexer_state}..{char_read_by_lookahead_lexer}.')
                if lookahead_lexer_state == 'STOP READING CHUNK DEFINITION NAME':
                    self.state = 'START READING CHUNK DEFINITION NAME'
                    break
                elif lookahead_lexer_state == 'STOP READING CHUNK DEFINITION EXTENSION NAME':
                    self.state = 'START READING CHUNK DEFINITION NAME'
                    break
                elif lookahead_lexer_state == 'STOP READING CHUNK REFERENCE NAME':
                    self.state = 'START READING CHUNK REFERENCE NAME'
                    break
                elif (lookahead_lexer_state not in ('PROSE', 'CODE')):
                    self.state = self.previous_state
                    break
        # We should not be in escape state after all this processing!
        if self.state == 'ESCAPE SEQUENCE':
            # print(f'ERROR! CHARACTER STILL CONSIDERED AN ESCAPE SEQUENCE: {self.previous_state}')
            self.state = self.previous_state
        elif self.state != self.previous_state:
            self.previous_state = self.state
        elif self.state == self.previous_state:
            if self.state == 'START READING CHUNK DEFINITION NAME':
                self.state = 'READING CHUNK DEFINITION NAME'
                # if self.char == '\n': self.char = ''
            elif self.state == 'STOP READING CHUNK DEFINITION NAME':
                self.state = 'CODE'
                self.reading_code = True
            elif self.state == 'STOP READING CHUNK DEFINITION EXTENSION NAME':
                self.state = 'CODE'
                self.reading_code = True
            elif self.state == 'START READING CHUNK REFERENCE NAME':
                self.state = 'READING CHUNK REFERENCE NAME'
                # if self.char == '\n': self.char = ''
            elif self.state == 'STOP READING CHUNK REFERENCE NAME':
                if self.reading_code is True: self.state = 'CODE'
                elif self.reading_code is False: self.state = 'PROSE'
            elif self.state == 'IGNORE':
                if self.char == '\n': self.state = 'CODE'
            elif self.state == 'NEW MODULE BEGINS':
                self.state = 'PROSE'
            elif self.state == 'RESET MODULE COUNTER':
                self.state = 'PROSE'
            elif self.state == 'COMMENT STARTS' and self.reading_code is True:
                self.state = 'READING COMMENT'
            elif self.state == 'COMMENT ENDS' and self.reading_code is True:
                self.state = 'CODE'
        lexer_result = (self.state, self.char)
        # print(f'Beforing returning, the previous state is {self.previous_state}')
        return lexer_result
    def is_reading_code(self):
        return self.reading_code
    def is_escape_sequence_escaped(self):
        return self.escape_sequence_escaped

# get_cmd_args_dict()
# Reads command line arguments and puts them in a dictionary as either options/switches or value of a switch
# depending on whether the argument starts with a hyphen or not
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

# get_chunk_name_map()
# This function is responsible for matching partial chunk names with the best possible full chunk name. This
# allows us to use three dots `...` after writing first few characters of a long chunk name. The partial
# chunk names are stored as keys and the corresponding full chunk names are stored as their values.  
def get_chunk_name_map(fname_list, markup_table):
    content = ''
    for fname in fname_list:
        with open(fname, 'r') as fp:
            content += ''.join(fp.readlines())
        content += '\n'
    # Create two sets: one which contains all chunk names (definitions + references) and the other one which
    # contains only those which do not end with '. . .'
    lexer = LitCodeLexer(content, markup_table)
    lexer.start()
    str_for_storing_chunk_name = ''
    all_chunk_names = set()
    all_full_chunk_names = set()
    chunk_name_map = dict()
    lexer_state = ''
    char_read_by_lexer = ''
    while (lexer_state != 'HALT'):
        lexer_result = lexer.read()
        lexer_state = lexer_result[0]
        char_read_by_lexer = lexer_result[1]
        # If you are reading a chunk's name
        if (lexer_state == 'READING CHUNK DEFINITION NAME' \
            or lexer_state == 'READING CHUNK REFERENCE NAME'):
            char_read_by_lexer = get_processed_char_when_reading_chunk_name(
                                        char_read_by_lexer, str_for_storing_chunk_name)
            str_for_storing_chunk_name += char_read_by_lexer
            # print(f'{char_read_by_lexer}')
            # print(f'{str_for_storing_chunk_name}')
        # Else if you have stopped reading a chunk's name
        elif (lexer_state == 'STOP READING CHUNK DEFINITION NAME' \
            or lexer_state == 'STOP READING CHUNK REFERENCE NAME'):
            all_chunk_names.add(str_for_storing_chunk_name)
            if not str_for_storing_chunk_name.endswith('...'):
                all_full_chunk_names.add(str_for_storing_chunk_name)
            str_for_storing_chunk_name = ''
    # print(all_chunk_names)
    # print(all_full_chunk_names)
    for chunk_name in all_chunk_names:
        if chunk_name in all_full_chunk_names and not chunk_name.endswith('...'):
            chunk_name_map[chunk_name] = chunk_name
        elif chunk_name not in all_full_chunk_names and chunk_name.endswith('...'):
            score = 0
            max_score = 0
            best_match = ''
            for full_chunk_name in all_full_chunk_names:
                phrase = chunk_name.strip('...')
                if (score := character_match_score(phrase, full_chunk_name)) > max_score:
                    max_score = score
                    best_match = full_chunk_name
            chunk_name_map[chunk_name] = best_match
    return chunk_name_map

# get_processed_char_when_reading_chunk_name()
# A chunk name, which could be either the name of a definition, extension or a reference can be split on
# multiple lines. We need to process it properly so that \n's and \t's are replaced by a single space only.
# This function does this job: when reading chunk definition/extension/reference name, call this function: it
# will return a character such that it does not insert 'bad' whitespaces in the chunk name.
def get_processed_char_when_reading_chunk_name(char_read_by_lexer, str_for_storing_chunk_name):
    if char_read_by_lexer in ('\n', '\t', ' '):
        if len(str_for_storing_chunk_name) > 0:
            if str_for_storing_chunk_name[-1] != ' ':
                char_read_by_lexer = ' '
            else:
                char_read_by_lexer = ''
    return char_read_by_lexer

# character_match_score()
# A function responsible for generating a score proportional to the number of
# characters in a string which match with those in a string it is supposed to be
# a part of. 
def character_match_score(phrase, full_string):
    score = 0
    if full_string.startswith(phrase):
        score = len(phrase) / len(full_string)
        score = round(score, 5)
    return score
