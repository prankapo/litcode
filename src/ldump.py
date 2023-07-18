#ldump.py: Starts at line 310 in ./web/source_code.web
#!/usr/bin/python3
import os
import sys
import re
import json

#ldump.py: Ends at 317 in ./web/source_code.web
#ldump.py: Extended at line 345 in ./web/source_code.web
def dumper(file_list):
    chunkDict = dict()
    for f in files:
#ldump.py: Reference at line 349 in ./web/source_code.web
        #Fill chunkDict: Starts at line 387 in ./web/source_code.web
        line_count = 0
        inChunk = False
        encounteredReference = False
        encounteredStopChar = False
        
        #Fill chunkDict: Ends at 393 in ./web/source_code.web
        #Fill chunkDict: Extended at line 399 in ./web/source_code.web
        with open(f, 'r') as fp:
            lines = fp.readlines()
        chunkLines = []
        
        #Fill chunkDict: Ends at 404 in ./web/source_code.web
        #Fill chunkDict: Extended at line 409 in ./web/source_code.web
        for line in lines:
            line_count += 1
        #Fill chunkDict: Reference at line 412 in ./web/source_code.web
            #Fill chunkDict: Not in a chunk: Starts at line 420 in ./web/source_code.web
            if not inChunk:
                chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
                if chunkname:
                    inChunk = True
            
            #Fill chunkDict: Not in a chunk: Ends at 426 in ./web/source_code.web
            #Fill chunkDict: Not in a chunk: Extended at line 432 in ./web/source_code.web
                chunkname = chunkname[0]
                if chunkname not in chunkDict:
                    chunkDict[chunkname] = []
                    chunkLines = []
                    chunkLines.append(f'@->{chunkname}: Starts at line {line_count} in {f}\n')
                else:
                    chunkLines = chunkDict[chunkname]
                    chunkLines.append(f'@->{chunkname}: Extended at line {line_count} in {f}\n')
            
            #Fill chunkDict: Not in a chunk: Ends at 442 in ./web/source_code.web
        #Fill chunkDict: Continues from line 413 in ./web/source_code.web
        #Fill chunkDict: Reference at line 413 in ./web/source_code.web
            #Fill chunkDict: In a chunk: Starts at line 450 in ./web/source_code.web
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
            #Fill chunkDict: In a chunk: Ends at 466 in ./web/source_code.web
        #Fill chunkDict: Continues from line 414 in ./web/source_code.web
        #Fill chunkDict: Ends at 414 in ./web/source_code.web
#ldump.py: Continues from line 350 in ./web/source_code.web
    chunkJSON = json.dumps(chunkDict, indent = 4)
    return chunkJSON

#ldump.py: Ends at 353 in ./web/source_code.web
#ldump.py: Extended at line 359 in ./web/source_code.web
def main():
    if len(sys.argv) <= 1:
        print('No files provided')
        exit(1)
    file_list = sys.argv[1:]
    json_str = dumper(file_list)
    print(json_str)

main()
#ldump.py: Ends at 369 in ./web/source_code.web

