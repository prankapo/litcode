"""
Here is the algorithm for litcode.
1. python3 litcode.py 'input directory' 'reference name' 'comment character'
2. Load the dictionary in Code class using TeX files present in the `input directory`. Go to the full depth.
3. Expand a reference name in the dictionary recursively.
"""

def expandref(ref, indentation = '', commentchar = '', use_tabs = False):
    """
    Go through the lines. 
    If you encounter something like @<\\coderef{blah blah}@> for codenv or 
    /*<\\coderef{yaka baka}>*/, then extract the name of the reference, compute the indentation and call
    yourself again. As you can see, I am too lazy to perform a typecheck.
    Return the indented string. 
    """
    global code_dict
    line_marker_flag = True
    try:
        linenum = code_dict[ref]['refstartlinenum']
    except KeyError:
        raise KeyError(f'{ref} is not a valid reference for a code/latex block in this directory')
    code_lines = ''
    for line in code_dict[ref]['lines']:
        if line_marker_flag is True:
            code_lines += f'{indentation}{commentchar}{code_dict[ref]["filename"]}'
            code_lines += f': {linenum}\n'
            line_marker_flag = False
        code_ref_extr = re.findall(r'(?<=^@<\\coderef{).+?(?=}@>\s*$)', line.lstrip())
        latex_ref_extr = re.findall(r'(?<=^/\*@\\coderef{).+?(?=}@\*/\s*$)', line.lstrip())
        extr = max(code_ref_extr, latex_ref_extr)
        if extr:
            extr = extr[0]
            current_indentation = line[:len(line) - len(line.lstrip())]
            if current_indentation:
                if use_tabs is True:
                    indentation += '\t'
                else:
                    indentation += current_indentation 
            code_lines += expandref(extr, indentation = indentation, commentchar = commentchar, use_tabs = use_tabs)
            line_marker_flag = True
            indentation = current_indentation
        else:
            code_lines += f'{indentation}{line}'
        linenum += 1
    return code_lines



code_dict = dict()

if len(sys.argv) < 4:
    raise Exception('Error in command!\nFormat: python3 litcode.py inputdir refname commentchar')

inputdir = sys.argv[1]
refname = sys.argv[2]
commentchar = sys.argv[3]
use_tabs = True
if '-tabs' in sys.argv:
    use_tabs = True

for (directory, subdirs, filelist) in os.walk(inputdir):
    for filename in filelist:
        if '.tex' not in filename:
            continue
        linenum = 0
        code_env = False
        latex_env = False
        chunk_ref = ''
        refs = dict()
        codelines = []
        fullfilename = directory + os.sep + filename
        fp = open(fullfilename, 'r')
        lines = fp.readlines()
        fp.close()
        for line in lines:
            linenum += 1
            if code_env is False and latex_env is False:
                extr_code_env = re.findall(r'(?<=^\\begin{code}\[).+?(?=\]\s*$)', line)
                extr_latex_env = re.findall(r'(?<=^\\begin{latex}\[).+?(?=\]\s*$)', line)
                extr = max(extr_code_env, extr_latex_env)
                if extr:
                    refstartlinenum = linenum
                    chunk_ref = extr[0]
                    if extr_code_env:
                        code_env = True
                    elif extr_latex_env:
                        latex_env = True
            elif code_env is True or latex_env is True:
                extr_code_end = re.findall(r'(^\\end{code}\s*$)', line)
                extr_latex_end = re.findall(r'(^\\end{latex}\s*$)', line)
                extr = max(extr_code_end, extr_latex_end)
                if extr:
                    refs[chunk_ref] = {
                                        'filename': fullfilename, 
                                        'refstartlinenum': refstartlinenum,
                                        'type': 'code',
                                        'lines': codelines
                                        }
                    if code_env is True:
                        refs[chunk_ref]['type'] = 'code'
                    elif latex_env is True:
                        refs[chunk_ref]['type'] = 'latex'
                    code_dict.update(refs)
                    code_env = False
                    latex_env = False
                    codelines = []
                else:
                    codelines.append(line)

jsonfile = open('./tests/dump.json', 'w')
json.dump(code_dict, jsonfile, indent = 4)
jsonfile.close()

lines = expandref(refname, commentchar = commentchar, use_tabs = use_tabs)
print(lines)

            self.file_path = ntpath.realpath(filename)
            os_type = platform.system()
            if os_type == 'Linux' or os_type == 'Darwin':
                self.file_path = self.file_path.replace('\\', '/')