# LitCode: Another Tool for Literate Programming

LitCode is a literate programming system/tool which I have developed. It follows noweb's markup style - Code
chunks begin with `<<Name of the chunk>>=`, end with `@`, and can be referenced, from both inside a chunk or
from a normal piece of text by enclosing the name of the chunk between `<<` and `>>`.  

# System Requirements
Hardware:
* Anything 64-bit will work

Software:
* Some *nix environment, preferrably Linux or WSL2
* gcc: For building and running the examples
* Python 3.8 or above along with pip: For installation and building the source and documentation
* latex: For generating the PDF
* texliveonfly: For installing missing LaTeX packages
* pdf2htmlEX: For converting a PDF to HTML

# Installation
To install LitCode, run:

```bash
make all
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