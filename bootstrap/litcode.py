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

class Cache:
    def __init__(self, dirname):
        self.dirname = dirname
        self.filenames = []
        self.cache_file = 'litcode.json'
        self.dict = {}
        # Now check whether the directory exists or not
        count = 0
        count_md = 0
        for (parent, subdirs, files) in os.walk(self.dirname):
            for f in files:
                count += 1
                if f.endswith('.md'):
                    count_md += 1
        print(f'{count} files detected.')
        print(f'{count_md} markdown files detected.')
        if count == 0:
            print(
                    '{dirname} is empty.'
                    '\nExiting...'
                )
            exit(4)
        if count_md == 0:
            print(
                    '{dirname} has no markdown files.'
            )
    
    def load_filenames(self):
        for (parent, subdirs, files) in os.walk(self.dirname):
            for f in files:
                self.filenames.append(parent + os.sep + f)
        # FOR DEBUGGING ONLY
        for f in self.filenames:
            print(f)
    
    def load_dict(self):
        # Check if it exists or not
        cache_file_not_found = False
        try:
            fp = open(self.cache_file, 'r')
            if not fp.readlines():
                cache_file_not_found = True
            fp.seek(0)
        except:
            cache_file_not_found = True
            print(f'Cache file {self.cache_file} not found. Creating it.')
            fp = open(self.cache_file, 'w+')
        # Load
        if not cache_file_not_found:
            self.dict = json.load(fp)
        else:
            print('No loading done')
        fp.close()
    
    def update_dict(self):
        cached_files_list = list(self.dict.keys())
        for filename in self.filenames:
            # Open the file and read all the lines inside it
            if not filename.endswith('.md'): continue
            fp = open(filename, 'r')
            lines = fp.readlines()
            fp.close()

            # Update the file's contents only if its modified time has been changed
            if filename not in cached_files_list:
                self.dict[filename] = {'modified-time': 0}
            modified_time = self.file_stat(filename) 
            if self.dict[filename]['modified-time'] != modified_time:
                self.dict[filename]['modified-time'] = modified_time
                self.dict[filename]['hasModified'] = True
            else:
                self.dict[filename]['hasModified'] = False
                continue
            
            # Store the chunks
            inChunk = False
            chunkname = ''
            encounteredReference = False
            encounteredStopChar = False
            chunkLines = []
            line_count = 0
            for line in lines:
                line_count += 1
                if encounteredReference:
                    chunkLines.append(line_count)
                    encounteredReference = False
                if not inChunk:
                    chunkname = re.findall(r'(?<=^<<).+?(?=>>=\s*$)', line.strip())
                    if chunkname:
                        chunkname = chunkname[0]
                        print(line)
                        inChunk = True
                        if chunkname not in self.dict[filename]:
                            self.dict[filename][chunkname] = []
                        chunkLines = []
                        chunkLines.append(line_count)
                        continue
                if inChunk:
                    encounteredStopChar = (line.strip() == '@')
                    if encounteredStopChar:
                        inChunk = False
                        self.dict[filename][chunkname] += chunkLines
                        continue
                    chunkLines.append(line)
                    reference = re.findall(r'(?<=^<<).+?(?=>>\s*$)', line.strip())
                    if reference:
                        reference = reference[0]
                        encounteredReference = True
                        continue
    
    def dump_dict(self):
        with open(self.cache_file, 'w') as fp:
            json.dump(self.dict, fp, indent = 4)
    
    def file_stat(self, filename):
        return os.path.getmtime(filename)

class Tangle:
    def __init__(self, dirname, refname):
        self.dirname = dirname
        self.refname = refname
        self.cache = Cache(dirname)
        self.tangling_rules = dict()
        self.chunkLines = ''
        self.cache.load_dict()
    
    def getref(self, filename, refname):
        self.chunkLines = self.expandref(filename, refname)
        whitespace_check_required = False
        if 'whitespace-mode' in list(self.tangling_rules[filename][refname].keys()):
            whitespace_check_required = True
            whitespace_mode = self.tangling_rules[filename][refname]['whitespace-mode']
            whitespace_number = self.tangling_rules[filename][refname]['whitespace-number']
        if whitespace_check_required and whitespace_mode == 'spaces-to-tabs':
            lines = ''
            for line in self.chunkLines.splitlines():
                indentation_depth = len(line) - len(line.lstrip(' '))
                new_indentation = '\t' * (indentation_depth // whitespace_number)
                new_indentation = ' ' * (indentation_depth % whitespace_number)
                line = new_indentation + line.lstrip()
                lines += line
            self.chunkLines = lines
        elif whitespace_check_required and whitespace_mode == 'tabs-to-spaces':
            lines = ''
            for line in self.chunkLines.splitlines():
                indentation_depth = len(line) - len(line.lstrip('\t'))
                new_indentation = ' ' * (whitespace_number)
                line = new_indentation + line.lstrip()
                lines += line
            self.chunkLines = lines
    
    def expandref(self, filename, refname = None, parent_indentation = ''):
        if refname not in list(self.cache.dict[filename].keys()):
            print(f'Chunk named {refname} not found!\nExiting...')
            exit(6)
        lines = ''
        for line in self.cache.dict[filename][refname]:
            # String
            if type(line) is str:
                indentation = line[:len(line) - len(line.lstrip())]
                # Reference
                reference = re.findall(r'(?<=^<<).+?(?=>>\s*$)', line.strip())
                if reference:
                    reference = reference[0]
                    lines += self.expandref(filename, reference, indentation)
                else:
                    lines += (parent_indentation + line)
            # Integer
            elif type(line) is int:
                lines += f'{self.tangling_rules[filename][refname]["comment-char"]}{line} in {filename}\n'
        return lines
    
    def writeref(self, destination):
        # First get the filename... build the path...
        # Do not forget to perform a system check!!
        # Finally write the file.
        dirname = ntpath.dirname(destination)
        fname = ntpath.basename(destination)
        if dirname:
            sbpr.call(['mkdir', '-p', dirname])
        with open(destination, 'w') as fp:
            fp.write(self.chunkLines)
        print(
                f'{len(self.chunkLines.splitlines())} lines written to '
                f'{destination}'
            )
    
    def tangle(self):
        for filename in list(self.tangling_rules.keys()):
            if self.cache.dict[filename]['hasModified'] is True:
                for refname in list(self.tangling_rules.keys()):
                    self.getref(filename, refname)
                    self.writeref(self.tangling_rules[filename][refname]['destination'])
    
    def force_tangle(self):
        for filename in list(self.tangling_rules.keys()):
            for refname in list(self.tangling_rules[filename].keys()):
                self.getref(filename, refname)
                self.writeref(self.tangling_rules[filename][refname]['destination'])
    
class Weave:
    def __init__(self):
        pass
    
    def transpiler(self):
        pass

def replace_whitespace(to_replace = 'tabs', n = 1):
    pass

def main():
    """
    Detect the mode of operation
    tangle: Tangle a reference
    weave: Hammer down the markdown file, replace special chars.
    update: Update the cache file. Should be done before every batch run.
    """
    mode = ''
    if sys.argv[1] == '-t' or sys.argv[1] == '--tangle':
        mode = 'tangle'
    elif sys.argv[1] == '-ft' or sys.argv[1] == '--force-tangle':
        mode = 'force-tangle'
    elif sys.argv[1] == '-w' or sys.argv[1] == '--weave':
        mode = 'weave'
    elif sys.argv[1] == '-u' or sys.argv[1] == '--update':
        mode = 'update'
    else:
        print('Mode of operation not specified. \nExiting...')
        exit(1)
    
    web_dirname = ''
    if '-I' in sys.argv:
        index = sys.argv.index('-I')
        web_dirname = sys.argv[index + 1]
    else:
        print('Input director not specified. \nExiting...')
        exit(2)
    
    if mode == 'update':
        cache = Cache(web_dirname)
        cache.load_filenames()
        cache.load_dict()
        cache.update_dict()
        cache.dump_dict()
    
    elif mode == 'tangle' or mode == 'force-tangle'
        if '-R' in sys.argv:
            index = sys.argv.index('-R')
            reference = sys.argv[index + 1]
        else:
            print('Tangle needs a reference to be extracted. None has been supplied. \nExiting...')
            exit(3)
        
        tangler = Tangle(web_dirname, refname)
        if '-cc' in sys.argv:
            index = sys.argv.index('-cc')
            commentchar = sys.argv[index + 1]
        
        else:
            print('No comment character provided. Defaulting to #')
            commentchar = '#'
        tangler.commentchar = '#'
    
        if '-ut' in sys.argv:
            index = sys.argv.index('-ut')
            whitespace_mode = 'spaces to tabs'
            whitespace_number = int(sys.argv[index + 1])
            tangler.whitespace_mode = 'spaces to tabs'
            tangler.whitespace_number = whitespace_number
        elif '-us' in sys.argv:
            index = sys.argv.index('-us')
            whitespace_mode = 'tabs to spaces'
            whitespace_number = int(sys.argv[index + 1])
            tangler.whitespace_mode = 'tabs to spaces'
            tangler.whitespace_number = whitespace_number
        tangler.tangle()
    
    elif mode == 'force-tangle':
        tangler = Tangle(web_dirname)
        tangler.force_tangle()
    
    elif mode == 'weave':
        weaver = Weave(web_dirname)
        weaver.transpiler()
    
main()