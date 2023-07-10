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
        self.cache_file = ''
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
        self.cache_file = self.dirname
        previous_filename = ''
        while (self.cache_file != previous_filename):
            previous_filename = self.cache_file
            self.cache_file = self.cache_file.strip('.')
            self.cache_file = self.cache_file.strip(os.sep)
        self.cache_file = self.cache_file.replace(os.sep, '-')
        self.cache_file = self.cache_file.replace('\\', '-')
        if self.cache_file == '':
            self.cache_file = 'parent'
        self.cache_file += '.json'
        print(f'Cache filename {self.cache_file}')
    
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
            else:
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
    def __init__(self):
        pass
    
    def load(self):
        pass
    
    def dump(self):
        pass
    
    def getref(self):
        pass
    
    def expandref(self):
        pass

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
    
    reference = ''
    commentchar = '#'
    whitespace_mode = 'tabs to spaces'
    whitespace_number = 4
    if mode == 'tangle':
        if '-R' in sys.argv:
            index = sys.argv.index('-R')
            reference = sys.argv[index + 1]
        else:
            print('Tangle needs a reference to be extracted. None has been supplied. \nExiting...')
            exit(3)
        
        if '-cc' in sys.argv:
            index = sys.argv.index('-cc')
            commentchar = sys.argv[index + 1]
        else:
            print('No comment character provided. Defaulting to #')
        
        if '-ut' in sys.argv:
            index = sys.argv.index('-ut')
            whitespace_mode = 'spaces to tabs'
            whitespace_number = int(sys.argv[index + 1])
        elif '-us' in sys.argv:
            index = sys.argv.index('-us')
            whitespace_mode = 'tabs to spaces'
            whitespace_number = int(sys.argv[index + 1])
        tangler = Tangle()

    if mode == 'weave':
        weaver = Weave()
        weaver.transpiler()
    
main()