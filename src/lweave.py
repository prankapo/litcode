#!/usr/bin/python3
import os
import sys
import re


def transpiler(lines):
    mode = 'Normal'
    chunkList = []
    processed_chunkList = []
    transpiled_lines = []
    
    for line in lines:
        chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
        if chunkname:
            chunkname = chunkname[0]
            if len(chunkname) != 0:
                chunkList.append(chunkname)
    
    for line in lines:
        if mode == 'Normal':
            chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
            if chunkname:
                chunkname = chunkname[0]
                if chunkname not in processed_chunkList:
                    mode = 'code'
                    processed_chunkList.append(chunkname)
                    envbegin = '\\begin{code}[' + chunkname + ']\n'
                    caption = '@<$\\langle$\\textit{' + chunkname + '}$\\rangle\\equiv$@>\n'
                else:
                    mode = 'oldcode'
                    envbegin = '\\begin{oldcode}\n'
                    caption = '@<$\\langle$\\textit{' + chunkname + '}$\\rangle ' + \
                                '\\thinspace +\\!\\!\\equiv$@>\n'
                transpiled_lines.append(envbegin)
                transpiled_lines.append(caption)
                continue
            
            vcodeBegins = (line.strip() == '<<>>=')
            if vcodeBegins:
                mode = 'vcode'
                envbegin = '\\begin{vcode}\n'
                transpiled_lines.append(envbegin)
                continue
            
            reference = re.findall(r'(?<=<<).+?(?=>>.*)', line.strip())
            if reference:
                reference = reference[0]
                if reference in chunkList:
                    line = line.replace('<<', '\\coderef{')
                    line = line.replace('>>', '}')
            
        
        elif mode == 'code' or mode == 'oldcode':
            buffer = ''
            i = 0
            while i < len(line):
                if line[i] == '@':
                    if i < len(line) - 1:
                        if line[i + 1] == '<' or line[i + 1] == '>':
                            buffer += '@<' + line[i] + line[i + 1] + '@>'
                            i += 2
                            continue
                buffer += line[i]
                i += 1
            line = buffer
            
            reference = re.findall(r'(?<=^<<).+?(?=>>\s*$)', line.strip())
            if reference:
                reference = reference[0]
                if reference in chunkList:
                    line = line.replace('<<', '@<\\coderef{')
                    line = line.replace('>>', '}@>')
            
            if line.strip() == '@':
                line = '\\end{' + mode + '}\n'
                mode = 'Normal'
            
        
        elif mode == 'vcode':
            if line.strip() == '@':
                mode = 'Normal'
                line = '\\end{vcode}\n'
            
        
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

