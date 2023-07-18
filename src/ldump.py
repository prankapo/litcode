#!/usr/bin/python3
import os
import sys
import re
import json

def dumper(file_list):
    chunkDict = dict()
    for f in file_list:
        line_count = 0
        inChunk = False
        encounteredReference = False
        encounteredStopChar = False
        
        with open(f, 'r') as fp:
            lines = fp.readlines()
        chunkLines = []
        
        for line in lines:
            line_count += 1
            if not inChunk:
                chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
                if chunkname:
                    inChunk = True
            
                    chunkname = chunkname[0]
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
    file_list = sys.argv[1:]
    json_str = dumper(file_list)
    print(json_str)

main()

