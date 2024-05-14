# LitCode24 - A Literate Programming Tool Written in Python 3

`Version 0.10`

## What is LitCode?
LitCode is a literate programming tool which has been written in Python 3. Unlike pre-existing literate
programming tools which are difficult to customize and understand, LitCode has been designed to give
programmers as much flexibility as possible to choose their own literate markup language and the markup
language in which the documentation for their code will eventually get generated in.

### A Digression: What is Literate Programming?
Traditionally, when we write a program, we write it a single structured implementation of a solution to some
problem. In this structure, we have several sub-structures like functions, methods, loops, conditional
statements, etc., all of which come together to get the problem solved.  

Literate programming is the philosophy of coding popularised by Donald Knuth. A literate program consists of
*modules*, in which we explain how we are solving a problem, our design decisions, and eventually write out some
*chunks* of structured code. These chunks are eventually *tangled* together to produce the source program. The
modules are *weaved* together properly to generate a documentation.  

I do not preach that literate programs are superior to traditional structured programs, but I can only present
my personal opinion that writing an algorithm as a literate program is much easier than writing it as a
structured program provided you have the correct tools. I was not able to understand the structure of Noweb
and did not like how it mangled the indentation of Python code whenever -L option was used. I wanted to write
a literate programming tool which has the following features:  

**A.** It is not tied to a single literate markup language. In LitCode, one can use Noweb style markup or
cook one up themselves by changing the markup table written by `linit`.  

**B.** The tool's woven output should not be tied to a single markup language like LaTeX or HTML. Again, a
basic structure of the markup language can be provided in a markup table written by `linit` and used with
`lweave`.  

**C.** The tool should be self-contained, and allow the user with a basic set of functions using which they
can extend the tool. LitCodeLexer, chunk name mapping functions, etc. are in `litcore.py` and can be imported
by the following statement:  

```Python
import litcode.litcore
```

## Installing LitCode
**REQUIREMENTS**: To install and properly test LitCode, ensure that your system has:  
1. Python 3.8 or above  
2. Pandoc 2.9 or above  
3. pdflatex (Can be installed by installing the TeX distribution for your system)  
4. Has a Unix environment with GNU Make and gcc installed (Windows user can use Cygwin, MSYS2, or WSL2)  

To install, download the source code and run:
```Bash
make install
```

Windows users running `make install` in CMD might encounter the following error:
```cmd
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from 
Settings > Manage App Execution Aliases.
```

They can run `make install-win` to install LitCode.  

Users running `make install` in macOS might encounter the following error:
```bash
python3 -m pip install . 
error: externally-managed-environment
```

They can run `make install-darwin` to install LitCode.  

## Uninstall LitCode
To uninstall LitCode, the following command can be run:
```Bash
make uninstall
```

If Windows users encounter the error due to Python3 alias mentioned in previous section, they can run the
following command to uninstall LitCode:  
```cmd
make uninstall-win
```

If macOS users encounter the error due to externally managed environment mentioned in the previous section,
they can run the following command to uninstall LitCode:  
```bash
make uninstall-darwin
```

## Testing LitCode
To test a version of a LitCode which has been installed in the system, you can run the following command in a
*NIX environment (Linux distro/WSL2/macOS):  
```bash
make tests
```

Windows users can run the following command for testing LitCode:  
```cmd
make tests-win
```

## Using LitCode
### Markup tables
There are two types of markup tables:  
**A.** Literate markup table: Symbols for marking up chunk name, references, etc., are defined in this table.  
**B.** Markup language markup table: Symbols for replacing the markup of literate markup table with those in
popular markup languages like markdown and LaTeX are defined in this table.  

Tables are first written using `linit`. Afterwards, you can write your program, and tangle and weave it using
`ltangle` and `lweave`, respectively.  

Usage of these Python scripts installed as console-scripts are now described briefly. This is the same content
which can be printed using `-h` or `--help` after installing LitCode.  

### linit
#### Purpose
Write markup tables to be used by either ltangle or lweave or litcode's extensions when processing file(s) 
containing literate programs.

#### Usage
```
linit -markup [markup language] -o [file(s)]
```

#### Example Usage
* `$ linit -o python.json c.json` writes the default literate markup table (similar to Noweb markup) to
  python.json and c.json.  
* `$ linit -markup markdown -o doc.json` writes the markup table used for markdown files to doc.json.  

#### Notes
1. If -markup option is not used, the default literate markup table gets written to the specified files.  
2. If a markup table has already been written to the file specified on command-line, the file is not
   rewritten. This avoids accidental overwriting of modifications made to a markup table by the user.  

#### Options
```
-o .......... Filename(s) to which the table is to be written   
-markup ..... Name of the markup table to be written  
              Available options:   
                    * literate:   for reading literate programs, similar to Noweb style.  
                    * markdown:   for literate programs written in markdown files  
                    * plain-text: for literate programs written in plain-text files  
                    * rst:        for literate programs written in restructured text files  
                    * tex:        for literate programs written in tex (or latex)  
              Literate markup table selected for a project will be used by both ltangle and lweave.   
              Markup tables specific for a markup language (example: markdown or tex) will be used only by  
              lweave for pretty printing.   
-h, --help .. Print brief documentation of linit  
```

### ltangle
#### Purpose
Tangle a code chunk out of file(s) containing literate programs and write it to the file(s) specified.

#### Usage
```
ltangle [file(s)] [-c chunk-name] [-lmt markup/table/to/use] \
        [-t tab-size] [-remindent indentation-level] \
        [-o output_file(s)]
```

#### Example Usage
* `$ ltangle common.txt program1.txt -c main.c -lmt lmt4c.json -t 4 -o main.c Archive/V0.34/main.c`  
* `$ltangle program1.txt common.txt -o init.c`  

#### Notes
1. If no chunk name is specified, the first chunk which is found in the literate programs is extracted.  
2. If no makrup table is specified, the default markup table for literate programming specified in litcore is
   used.  
3. If no output files are specified to which the tangled source code is to be written, ltangle will operate in
   debug mode. In debug mode, the dictionary of chunk definitions and tangled lines are printed on screen.   
4. If -t option is not used, tabs used for indentation are replaced by 4 spaces.  

#### Options
```
-c .......... Name of the code chunk to be tangled  
-o .......... Name of the file(s) to which the tangled code is to be written  
-lmt ........ Markup table to be used during tangling  
-h, --help .. Print brief documentation of ltangle  
-t .......... Replace n spaces by tabs  
-rind ....... Replace r level(s) of indentation  
-rnul ....... Do not include lines containing only whitespace in tangled output  
-L .......... Insert line number (in literate program) from which the source line originates as a comment  
```

### lweave
#### Purpose
Tangle a code chunk out of file(s) containing literate programs and write it to the file(s) specified.

#### Usage
```
lweave [file(s)] [-lmt literate/markup/table/to/use] [-mmt markup/table/to/use] \
        [-o output_file(s)]
```

#### Example Usage
* `$ lweave common.txt program1.txt -lmt lmt4c.json -mmt md.json -o Program1.md`  
* `$ lweave common.txt program1.txt -o Program1.txt`  

#### Notes
1. If no literate markup table is provided, then the default markup table for literate programming defined in
   litcore is used.  
2. If no markup table (for a markup language) is specified, then the markup table for plain-text is used.   
3. If -o option is not used, woven output will be printed on the screen.   

#### Options
```
-o .......... Name of the file(s) to which the tangled code is to be written
-lmt ........ Markup table containing symbols used for marking elements of a literate program
-mmt ........ Markup table containing symbols of markup language used
-h, --help .. Print brief documentation of lweave
```

## Contributing
I have found programming in literate fashion to be a joy. I hope that those who use this tool also do find
this programming methodology to be joyful. I would love to hear the suggestions of users who have used LitCode
and how it can be improved. You can drop me a mail at `kapoorpraneet2619@gmail.com`.
