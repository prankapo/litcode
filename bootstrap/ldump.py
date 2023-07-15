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

"""
Format of using the command:
ldump space separated list of files > name/of/json/file
"""

def dumper(files):
    chunkDict = dict()
    for f in files:
        inChunk = False
        chunkLines = []
        encounteredReference = False
        encounteredStopChar = False
        line_count = 0
        with open(f, 'r') as fp:
            lines = fp.readlines()
        for line in lines:
            line_count += 1
            if not inChunk:
                chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
                if chunkname:
                    chunkname = chunkname[0]
                    inChunk = True
                    if chunkname not in chunkDict:
                        chunkDict[chunkname] = []
                        chunkLines = []
                        chunkLines.append(f'@->{chunkname}: Starts at line {line_count} in {f}\n')
                    else:
                        chunkLines = chunkDict[chunkname]
                        chunkLines.append(f'@->{chunkname}: Extended at line {line_count} in {f}\n')
            else:
                encounteredStopChar = (line.strip() == '@')
                if encounteredStopChar:
                    chunkLines.append(f'@->{chunkname}: Ends at {line_count} in {f}\n')
                    chunkDict[chunkname] = chunkLines
                    inChunk = False
                    continue
                else:
                    encounteredReference = re.findall(r'(?<=^<<).+?(?=>>\s*$)', line.strip())
                    if encounteredReference:
                        chunkLines.append(f'@->{chunkname}: Reference at line {line_count} in {f}\n')
                        chunkLines.append(line)
                        chunkLines.append(f'@->{chunkname}: Continues from line {line_count + 1} in {f}\n')
                    else:
                        chunkLines.append(line)
    chunkJSON = json.dumps(chunkDict, indent = 4)
    return chunkJSON

def main():
    if len(sys.argv) <= 1:
        print('No files provided')
        exit(1)
    files = sys.argv[1:]
    json_str = dumper(files)
    print(json_str)

main()