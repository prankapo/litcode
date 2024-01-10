#!/usr/bin/python3
import os
import sys
import time

import re
import math

import ntpath
import platform
import subprocess as sbpr

import json

# If you encounter a chunk
# Check if it has been defined previously or not
# Convert it.
# Inside a chunk
# Check if the chunk has been ended '@'
# If you encounter a reference
# Use \coderef to refer to it.
# If in a normal line you encounter <<>> in a normal line outside of a chunk, use coderef.
def transpiler(lines):
    chunkList = []
    inChunk = False
    code = False
    oldcode = False
    transpiled_lines = []
    for line in lines:
        if not inChunk:
            chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
            if chunkname:
                inChunk = True
                chunkname = chunkname[0]
                if chunkname not in chunkList:
                    chunkList.append(chunkname)
                    envbegin = '\\begin{code}[' + chunkname + ']\n'
                    caption = '@<$\\langle$\\textit{' + chunkname + '}$\\rangle\\equiv$@>\n'
                    code = True
                elif chunkname in chunkList:
                    envbegin = '\\begin{oldcode}\n'
                    caption = '@<$\\langle$\\textit{' + chunkname + '}$\\rangle ' + \
                                '\\thinspace +\\!\\!\\equiv$@>\n'
                    oldcode = True
                transpiled_lines.append(envbegin)
                transpiled_lines.append(caption)
                continue
        elif inChunk:
            if line.startswith('@'):
                if code:
                    transpiled_lines.append('\\end{code}\n')
                    code = False
                elif oldcode:
                    transpiled_lines.append('\\end{oldcode}\n')
                    oldcode = False
                inChunk = False
                continue
            # Escape the escape characters.
            #line = line.replace('@<', '@<@<@>')
            #line = line.replace('@>', '@<@>@>')
            buffer = ''
            iterator = iter(range(len(line)))
            for i in iterator:
                if i < len(line) - 1 and ('@<' in line or '@>' in line):
                    if line[i] + line[i + 1] == '@<':
                        buffer += '@<@<@>'
                        i = next(iterator)
                    elif line[i] + line[i + 1] == '@>':
                        buffer += '@<@>@>'
                        i = next(iterator)
                else:
                    buffer += line[i]
            line = buffer
        reference = re.findall(r'(?<=<<).+?(?=>>.*)', line.strip())
        if reference:
            reference = reference[0]
            if inChunk:
                line = line.replace('<<', '@<\\coderef{')
                line = line.replace('>>', '}@>')
            else:
                line = line.replace('<<', '\\coderef{')
                line = line.replace('>>', '}')
        transpiled_lines.append(line)
    return transpiled_lines

def main():
    if len(sys.argv) < 2:
        print('File names have to be provided as command line arguments')
        exit(1)
    files = sys.argv[1:]
    lines = []
    transpiled_lines = []
    for file in files:
        with open(file, 'r') as fp:
            lines += fp.readlines()
    transpiled_lines += transpiler(lines)
    print(''.join(transpiled_lines))

main()