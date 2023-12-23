# LitCode: Another Tool for Literate Programming

LitCode is a literate programming system/tool which I have developed. It follows noweb's markup style - Code
chunks begin with `<<Name of the chunk>>=`, end with `@`, and can be referenced, from both inside a chunk or
from a normal piece of text by enclosing the name of the chunk between `<<` and `>>`.  

# System Requirements

The program was developed on a machine running Ubuntu 22.04, and, therefore, I have assumed that you will be
running a Linux system (or WSL or something). With most Linux distros, you generally get some version of
Python 3. The program which I have written doesn't require any system-breaking methods, so any version of
Python 3 > 3.8 should work fine. You will also need to have LaTeX, `texliveonfly`, and `pdf2htmlEX` installed
in your system. Finally, you need to have a `~/local/bin` directory which you have set to path in your bashrc file.

# Installation

To install LitCode, run:

```bash
make install
```

Once installed, you can run the weave the documentation:

```bash
make documentation
make buildtex
```

You can build the examples that are there in the documentation:

```bash
make examples
make runex
```

# Example Usage

Just write your web files using noweb markup style. To generate `litcode.sty` in a directory, say
`documentation/`, run:

```bash
linit documentation/
```

Before tangling, you need to generate a JSON dump of all the chunks in the files. 

```bash
ldump file1.web file2.web file3.web > src.json
```

Now you can run tangle to extract the source code.

```bash
ltangle -i src.json -R main.c -cc '//' > src/main.c
ltangle -i src.json -R Makefile -cc '#' -ut 4 > src/Makefile
```

To generate a LaTeX file, run the following:

```bash
lweave file1.web file2.web file3.web > documentation/content.tex
```

`lweave` won't include a preamble in its output. You have to write a 'container' `tex` file yourself. Don't
forget to include `\usepackage{litcode}` in it!