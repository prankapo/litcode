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
litcode -dir dirname -r refname -c commentchar -use_tabs

-d --dir
-r --ref
-cc --comment-char
-ut --use-tabs

Example: litcode -dir tests -r basic_indentation_test -c '%' -use_tabs 4
Do os.path.basename(refname)
mkdir -p os.path.dirname(refname)

Also: refname should be included as part of comments during expansion.
"""
class CodeDict:
    def __init__(self):
        self.code_dict = dict()
        self.dirname = ''
        self.refname = ''
        self.commentchar = ''
        self.use_tabs = False
        self.spaces = 0
        self.lines = ''
        if '-d' in sys.argv or '--dir' in sys.argv:
            i = None
            try:
                i = sys.argv.index('-d')
            except:
                i = sys.argv.index('--dir')
            self.dirname = sys.argv[i + 1].rstrip(os.sep)
        else:
            print('Directory name not found as a cmd arg.')
            exit(1)
        
        if '-r' in sys.argv or '--ref' in sys.argv:
            i = None
            try:
                i = sys.argv.index('-r')
            except:
                i = sys.argv.index('--ref')
            self.refname = sys.argv[i + 1]
        else:
            print('Reference name not found as a cmd arg.')
            exit(1)
        
        if '-cc' in sys.argv or '--comment-char' in sys.argv:
            i = None
            try:
                i = sys.argv.index('-cc')
            except:
                i = sys.argv.index('--comment-char')
            self.commentchar = sys.argv[i + 1]
        
        if '-ut' in sys.argv or '--use-tabs' in sys.argv:
            self.use_tabs = True
            i = None
            try:
                i = sys.argv.index('-ut')
            except:
                i = sys.argv.index('--use-tabs')
            self.spaces = int(sys.argv[i + 1])
    
    def load(self):
        for (dirname, subdirs, files) in os.walk(self.dirname):
            for fname in files:
                if not fname.endswith('.tex'):
                    continue
                refs = self.build_code_dict(dirname, fname)
                self.code_dict.update(refs)
    
    def dump(self):
        with open('litcode-dump.json', 'w') as fp:
            json.dump(self.code_dict, fp, indent = 4)
    
    def build_code_dict(self, dirname, fname):
        refs = dict()
        lno = 0
        refname = ''
        chunk = []
        inChunk = False
        inline_ref_flag = False
        fname = dirname + os.sep + fname
        with open(fname, 'r') as fp:
            lines = fp.readlines()
        for line in lines:
            lno += 1
            if not inChunk:
                refname = max(
                                    re.findall(r'(?<=^\\begin{code}\[).+?(?=\]\s*$)', line.lstrip()),
                                    re.findall(r'(?<=^\\begin{latex}\[).+?(?=\]\s*$)', line.lstrip())
                                    )
                if refname:
                    chunk = []
                    inChunk = True
                    refs[refname[0]] = {
                                    'srcfname': fname,
                                    'dstfname': refname[0],
                                    'startlno': lno,
                                    'lines': []
                    }
                    chunk.append(f'{self.commentchar} "{fname}" line {lno}\n')
                    chunk.append(f'{self.commentchar} {refname}\n')
            elif inChunk:
                chunk_end = max(
                                    re.findall(r'(^\\end{code}\s*$)', line.lstrip()),
                                    re.findall(r'(^\\end{latex}\s*$)', line.lstrip())
                                    )
                if chunk_end:
                    inChunk = False
                    refs[refname[0]]['lines'] += chunk
                else:
                    if inline_ref_flag is False:
                        inline_ref = max(
                                        re.findall(r'(?<=^@<\\coderef{).+?(?=}@>\s*$)', line.lstrip()),
                                        re.findall(r'(?<=^/\*@\\coderef{).+?(?=}@\*/\s*$)', line.lstrip())
                                        )
                        if inline_ref:
                            inline_ref_flag = True
                    elif inline_ref_flag is True and line.strip() != '':
                        inline_ref_flag = False
                        indentation = line[:len(line) - len(line.lstrip())]
                        chunk.append(f'{indentation}{self.commentchar} "{fname}" line {lno}\n')
                        chunk.append(f'{indentation}{self.commentchar} {refname}\n')
                    chunk.append(line)
        return refs
    
    def replace_spaces_with_tabs(self):
        if not self.use_tabs:
            return
        lines = ''
        for line in self.lines.splitlines():
            indentation_depth = len(line) - len(line.lstrip(' '))
            new_indentation = '\t' * (indentation_depth // self.spaces)
            new_indentation += (' ' * (indentation_depth % self.spaces))
            line = line.lstrip(' ')
            line = new_indentation + line + '\n'
            lines += line
        self.lines = lines
    
    def getref(self):
        self.lines = self.expandref()
        self.replace_spaces_with_tabs()
    
    def expandref(self, refname = None, parent_indentation = ''):
        if refname is None:
            refname = self.refname
        if not refname in list(self.code_dict.keys()):
            print(f'"{refname}" not found!!')
            exit(1)
        lines = ''
        for line in self.code_dict[refname]['lines']:
            inline_ref = max(
                                    re.findall(r'(?<=^@<\\coderef{).+?(?=}@>\s*$)', line.lstrip()),
                                    re.findall(r'(?<=^/\*@\\coderef{).+?(?=}@\*/\s*$)', line.lstrip())
                                    )
            if inline_ref:
                indentation = line[:len(line) - len(line.lstrip())]
                lines += self.expandref(refname = inline_ref[0], parent_indentation = indentation)
            else:
                lines += (parent_indentation + line)
        return lines
    
    """
    A function for replacing spaces with tabs...get ref calls it in the end.... No predefined changes... in
    build_code_dict(). getref() should do it with the assembled code!!
    include indentation of reference in the code block....
    """
    
    def printref(self):
        print(self.lines)
    
    def writeref(self):
        # First get the filename... build the path...
        # Do not forget to perform a system check!!
        # Finally write the file.
        dirname = ntpath.dirname(self.code_dict[self.refname]['dstfname'])
        fname = ntpath.basename(self.code_dict[self.refname]['dstfname'])
        if dirname:
            sbpr.call(['mkdir', '-p', dirname])
        with open(self.code_dict[self.refname]['dstfname'], 'w') as fp:
            fp.write(self.lines)
        print(f'{len(self.lines.splitlines())} lines written to {self.code_dict[self.refname]["dstfname"]}')

litcode_main = CodeDict()
litcode_main.load()
# Load -> build_code_dict()
litcode_main.dump()
litcode_main.getref()
# getref -> expandref()
#litcode_main.printref()
litcode_main.writeref()