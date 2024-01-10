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

def expandref(chunkDict, reference):
    codeLines = []
    encounteredReference = False
    indentation = ''
    for line in chunkDict[reference]:
        encounteredReference = re.findall(r'(?<=^<<).+?(?=>>\s*$)', line.strip())
        if encounteredReference:
            reference = encounteredReference[0]
            encounteredReference = True
            buffer = expandref(chunkDict, reference)
            indentation = line[:len(line) - len(line.lstrip())]
            for l in buffer:
                line = indentation + l
                codeLines.append(line)
        else:
            codeLines.append(line)
    return codeLines

def main():
    dumpfile = str()
    reference = str()
    commentchar = None
    usetabs = False
    whitespace_conv_num = 4
    if '-i' in sys.argv:
        i = sys.argv.index('-i')
        dumpfile = sys.argv[i + 1]
    else:
        print('Cannot find -i flag')
        exit(1)
    if '-R' in sys.argv:
        i = sys.argv.index('-R')
        reference = sys.argv[i + 1]
    else:
        print('Cannot find -R flag')
        exit(1)
    if '-cc' in sys.argv:
        i = sys.argv.index('-cc')
        commentchar = sys.argv[i + 1]
    if '-ut' in sys.argv:
        usetabs = True
        i = sys.argv.index('-ut')
        whitespace_conv_num = int(sys.argv[i + 1])
    if '-us' in sys.argv:
        usetabs = False
        i = sys.argv.index('-us')
        whitespace_conv_num = int(sys.argv[i + 1])
    
    # This is the portion where we can load the JSON file
    chunkDict = dict()
    with open(dumpfile, 'r') as fp:
        chunkDict = json.load(fp)
    
    # Now we call the expandref function
    codeLines = expandref(chunkDict, reference)
    #print(''.join(codeLines))

    # Now replace '@->' with comment character
    lines = []
    for line in codeLines:
        # Spaces to Tabs
        if usetabs is True:
            indentation_depth = len(line) - len(line.lstrip(' '))
            # This condition is required, otherwise for indentation_depth = 0, all
            # indentation will be eaten away.
            if indentation_depth:
                new_indentation = '\t' * (indentation_depth // whitespace_conv_num)
                new_indentation += ' ' * (indentation_depth % whitespace_conv_num)
                line = new_indentation + line.lstrip()
        # Tabs to Spaces
        elif usetabs is False:
            indentation_depth = len(line) - len(line.lstrip('\t'))
            if indentation_depth:
                new_indentation = ' ' * (indentation_depth * whitespace_conv_num)
                line = new_indentation + line.lstrip()
        if line.lstrip().startswith('@->'):
            if commentchar is not None:
                line = line.replace('@->', commentchar, 1)
            else:
                continue
        lines.append(line)
    codeLines = lines

    # Now print it
    print(''.join(codeLines))

main()