# LitCode - Another Tool for Literate Programming

*Author:* Praneet Kapoor  

*Date:* 05 February, 2024  

LitCode is a tool for literate programming which I have developed so as to enable me to provide better
exposition to myself for a particular piece of code when I look at it after months or years. It is made up of
very simple console-scripts written in Python. The functionality of the scripts can be tinkered with by
playing a translation dictionary (nothing but a JSON file) and some `hooks` written in Python, and executed
using ever dangerous `exec()`.

<!-- START doctoc -->
<!-- END doctoc -->

# Introduction
Traditional programming involves writing a code in some language $L$, in some file $F$ to solve a particular
problem or set of problems $P$. What was the big problem which I was attempting to solve by creating this project?

Let it be known to the reader that *LitCode* was created just to solve the problems that I have
faced while working and maintaining my own projects. It wasn't made with any grandiose aim of [making the world a
better place](https://youtu.be/B8C5sjjhsso?si=y7wyOdbuodoHT4cv).

Then, what problems was I aiming to solve by this product of self-indulgence? 

Let me ask you, the reader, the following questions:  

1. When you were coding, did you ever felt like inserting a lot of comments to explain every bit of code? No?
	Well, good for you! I, on the other hand, always have this urge to explain everything in my code to some
	alien ten thousand years in the future who happens to stumble upon my projects.  

2. Did you ever felt like the information you were digesting while cooking something up, or the rush with
	which new ideas were coming to your mind was too much? Still no? As for me, my working memory seems to be
	pathetic. I find it hard to keep on cleaning my code while adding some feature which pops up in my head.  

3. Ok, I think that you and I can relate on this: Did you ever felt like you were a genius or too stupid when
	you review a piece of code you wrote months back and fail to remember why you did something the way your
	past-self did? Still no? I ENVY YOU!.	

Well, these are the problems I was facing while working on some big projects during my undergraduate years.
The solution was to come up with a way of writing programs using which I can explain myself the routes I took,
the pitfalls and the victories while solving some problem. This methodology of writing programs is called
*Literate programming*. I didn't come up with it: Donald Knuth, [the Yoda of Computer
Science](https://www.nytimes.com/2018/12/17/science/donald-knuth-computers-algorithms-programming.html) came
up with it while he was working on \TeX{} typesetting system. And I like it. It doesn't matter whether the world
adopts this methodology or not, but I like it. I was feeling burned-out working from 9 - 6 and then trying to get
myself to do some programming. This little change in programming style has helped me keep a track of ideas
even when my brain is firing only its last neuron.

Enough of this self-explanation and let me tell you what literate programming is. 


## What is Literate Programming? 
 The first program which a person, who has begun to learn a particular language, is intended to solve the
problem of printing the string *Hello, world* on the screen. This problem can be solved easily: using some
function defined in the standard input-output library which comes with the toolchain for the language, you
simply print the string *Hello, world!*. For example, in C, you can use `printf` defined in `stdio.h` to
accomplish this task. 
```C
#include <stdio.h>

int main() {
	printf("Hello, world!\n");
	return 0;
}
```

In Python, you can use `print` which is a part of the standard library which comes with the Python toolchain.
```Python
print("Hello, world")
```

These programming, or rather *problem-solving* tasks, are pretty simple. But as one will learn more and more
about a particular language, they will start solving problems which are more and more complex. As his or her
knowledge advances, it is highly likely that the student will be given the task to print $n$ prime numbers. In
C, we can write the following piece of code:

```C
#include <stdio.h>
#include <stdlib.h>


int main(int argc, char ** argv) {
	int n;
	if (argc < 2) {
		fprintf(stdout, "Pass the number of primes to be generated!\n");
		return 1;
	}
	n = atoi(argv[1]);

	int N, d, is_prime, prime_count;
	prime_count = 0;
	N = 2;
	while (prime_count < n) {
		is_prime = 0;
		for (d = 2; d < (N / 2); ++d) {
			if (N % d == 0) {
				is_prime = 1;
				break;
			}
		}

		if (is_prime == 0) {
			++prime_count;
			fprintf(stdout, "%4d.\t%8d\n", prime_count, N);
		}
		++N;
	}

	return 0;
}
```

There are people who can with one glance be able to tell what the above program does. I am able to do that at
times, but I still want to tell myself everytime I read the program what each line in it does and if it is
correct or not. If someone were to throw a brick on my head, I might end up forgetting the meaning of `atoi()`
and [how harmful it is and how using `strtol()` is the mark of a real
gentleman](https://stackoverflow.com/questions/17710018/why-shouldnt-i-use-atoi#:~:text=With%20the%20atoi%20there%20is,32%20bits%20on%20most%20platforms).
Keeping everything in your memory while working on a project became a real hinderence when I worked on some
'big' projects during my undergrad, like a PID controller for ball balancing platform, or a sick cousin of
MS-DOS in 8086 assembly language. In larger projects, it is a practice to write programs in multiple files in
order to take off the load of our minds and make the process of debugging simpler: it is easier to debug 5
files containing 500 lines of code than to debug a file containg 2500 lines of code.  

Even after I stopped writing monoliths and started embracing libraries and object files, I still felt a need
to tell myself everytime I entered a line about its purpose. I wanted to record why I made some decisions and
where all I have failed to get the desired result. Much like the pages on the workbook, on which you go to
left, then to right, then to top and bottom and scratch a lot before finding the solution to a particularly
nasty integral, I felt that a program should tell the story on how the solution was reached.  

Thankfully, I am not alone in this desire to for exposition intermixed with every step taken while writing a
program. Donald Knuth also felt the need for telling a story when working on his big projects (maybe a problem
faced only with people inclined towards academia and low-level stuff). So, he came up with the concept of
literate programming. He called it literate for two reasons:  

1. Knuth considers writing program as an art form and as works of literature.  

2. Knuth felt he was coerced into accepting the ideas of *structure programming* because he felt it would be
	pathetic to be found guilty of writing *unstructured program*. So, to quote him,

> *Now I have a chance to get even. By coining the phrase "literate programming," I am imposing a moral
> commitment on everyone who hears the term; surely nobody wants to admit writing an illiterate program.*


## How does one write a literate program?
A literare program involves presenting code and associated in the order which makes it easier for a human to
deal with it, while both developing and understanding it. A source file containing a literate program, often
called a *WEB* file (as it has a web of ideas), can be broken down into modules or sections, each explaining a
particular idea behind something in the code. It is often nice to have these sections numbered. In fact, these
sections are a generalized version of what we call as *cells* in a Notebook. A cell can contain either prose
or a *chunk* of source code, or both. These *chunks* are often named and can be referenced using their name.
Each time you define a chunk with the same name, you keep on extending its defintion.  

So, you now have a file with lots of modules and some of them have chunks of program. How can you assemble the
source code out of this? To do that we have to *tangle our web of ideas* which is called *tangling*. In the
original WEB system which Knuth had developed back in 80's, this job of tangling the WEB file to generate the
source file is done by a program called, unsuprisingly, `tangle`. In the CWEB system developed by Don Knuth
and Silvio Levy, tangling is done by `ctangle`. In noweb, a much simpler literate programming system developed
by Norman Ramsey, tangling is done by `notangle`. And in LitCode, it will be done by `ltangle`.  

The job of generating a beautifully typeset documentation is called *weaving the web* and, in the OP WEB
system, it is done by a software called `weave`. In CWEB and noweb, it is done by `cweave` and `noweave`,
respectively. In LitCode, weaving will be done by `lweave`.  

Figure \ref{fig:lpw} should give you an idea of the workflow when working with a literate
programming system. This workflow is being used in LitCode too.  

![Literate Programming Workflow\label{fig:lpw}](figures/literate_workflow.png){width=350px}

Feeling that my explanation about literate programming workflow is inadequete, I now present an extract from
*Mathematical Writing (1987): Notes from class, October 21* by Paul Roberts summarizing the lectures of Knuth
during the autumn of 1987:

> *Don showed us his thick book TEX: The Program-a listing of the code for TEX, written in WEB. It consists
> of almost 1400 modules. The guiding principle behind WEB is that each module is introduced at the
> psychologically right moment. This means that the program can be written in such a way as to motivate the
> reader, leaving TANGLE to sort everything out later on. [The TANGLE processor converts WEB programs to Pascal
> programs.] After all, we don't need to worry about motivating the compiler. (Don added the aside that contrary
> to superstition, the machine doesn't spend most of its time executing those parts of the code that took us the
> longest to write.) It seems to be true that the best way in which to present program constructs to the reader
> is to use the same order in which the creator of the program found himself making decisions about them. Don
> himself always felt it was quite clear what had to be presented next, throughout the entire composition of
> this huge program. There was at all points a natural order of exposition, and it seems that the natural
> orderings for reading and writing are very much the same.*


## An Example of a Literate Program: Print first $n$ Prime Numbers
Sometimes a concept is better understood with an example. Literate programming is one such concept. It is time
to give an example of a literate program so that the reader can understand how it differs from a normal
program. I will be rewriting the program for printing first $n$ prime numbers in a literate manner. This will
allow the reader to contrast this approach with the time-tested traditional approach of writing a program.  

### `generate_primes.c`
@ A number is said to be prime if it has no divisors other than 1 and itself. A simple way of checking whether
a given number $N$ is prime or not is to see if it has more than one divisors in the set $\{1, 2, \ldots , N -
1\}$. If it has, then it is not a prime, else it is one. With a little more thought we can see that our list
does not need to go till $N - 1$; we just need to check for the divisors till $\lfloor\frac{N}{2}\rfloor$. In
fact, we can even remove 1 from this set, for every number is divisible by 1. We now have a rough sketch of
how we will check whether a number is prime or not: let $d$ be iteratively set to values in the sequence $\{2,
3, \ldots , \lfloor\frac{N}{2}\rfloor\}$, starting from 2. We see if $N\;\texttt{\%}\;d$ is equal to zero for any
number in this set, then $N$ is not a prime number. Else, if we exhaust this set and fail to find a divisor
for $N$, then $N$ is a prime number.  

@ We need to also print the prime number and keep a tab of how many prime numbers we have encountered so far.
This can be done by resetting a flag every time we go into our `check for divisors` loop. This flag is set to
1, if the number is **not** a prime, and then we break from the loop. Outside the loop, if this flag is 0,
then we can print out the number and iterate a counter (keeping tabs of the number of primes we have
encountered). If the counter is less than $n$, we can increment $N$ by 1. Else, we break from the computation
and end the program.  

@ We have now have a well developed vague picture of how our program should work. So, let's write down the
core of our program.  

<<Generate n prime numbers>>=
```C
int N, d, is_prime, prime_count;
prime_count = 0;
N = 2;
while (prime_count < n) {
	is_prime = 0;
	<<Check if N is prime or not>>
	if (is_prime == 0) {
		++prime_count;
		fprintf(stdout, "%4d.\t%8d\n", prime_count, N);
	}
	++N;
}
```
  
@ <<Check if N is prime or not>>=	
```C
for (d = 2; d <= (N / 2); ++d) {
	if (N % d == 0) {
		is_prime = 1;
		break;
	}
}
```

@ Having figured out the solution to our problem, we can now define the layout of chunks in our program:  

<<generate_primes.c>>=
```C
<<Include libraries>>

int main(int argc, char ** argv) {
	<<Read n from command-line>>
	<<Generate n prime numbers>>
	return 0;
}
```

@ When it comes to the libraries, we of course need `stdio.h`. If we need another one, we can simply add it
to the chunk.  

<<Include libraries>>=
```C
#include <stdio.h>
```

@ Our program will take a single command line argument, $n$. Now, this argument would be a character string.
For our purposes, we can use often frowned upon `atoi()` function defined in `stdlib.h` and proceed from
there. First we include `stdlib.h` in <<Include libraries>>.  

<<Include libraries>>=
```C
#include <stdlib.h>
```

@ Now we can write down <<Read n from command-line>>, which will be responsible for reading $n$ from the
command-line. We need to make sure that we throw some error in case no input has been provided. This can be
done by checking the value of argc: if its less than 2, then only the name of the program was entered in the
command-line and nothing else, in which case we simply exit after printing an error message:	 

<<Read n from command-line>>=
```C
int n;
if (argc < 2) {
	fprintf(stdout, "Pass the number of primes to be generated!\n");
	return 1;
}
n = atoi(argv[1]);
```

@@

### Building and running the program
@ To build and run `generate_primes.c`, we can use a Makefile. Let's call it *make_example.mk*. It will have the
following structure:  

<<make_example.mk>>=
```Makefile
<<Define compiler and C flags>>
<<Test run>>
<<Build rule>>
<<Remove generate_primes.exe>>
```

@ I will be using `-std=c99` and not `-ansi -pedantic` for the latter uses K&R C style strictly and won't
allow me to define variables freely anywhere in a function. Also, I will optimize it using -O2 flag, because
hey! user can go wild and ask it to print a million prime numbers.  

<<Define compiler and C flags>>=
```Makefile
CC: gcc -std=c99 -O2
```

@ To build this program, we can simply pass it to the compiler and use -o flag to get an executable.  

<<Build rule>>=
```Makefile
generate_primes.exe: generate_primes.c
	$(CC) generate_primes.c -o generate_primes.exe
```

@ And to test it, we can define another rule, <<Test run>>.		

<<Test run>>=
```Makefile
test: generate_primes.exe
	./generate_primes.exe 10
```

@ Note that as I am using a Linux environment for developing this code, I am running the program by appending
`./` in front of it. If you are using Windows command prompt (assuming you have gcc installed), then you can
use the target for `test_win` for testing on Windows.  

<<Test run>>=
```Makefile
test_win: generate_primes.exe
	generate_primes.exe 10
```

@ Finally, after all this, it is a good habit to clean the directory. `clean` will help you do that:  

<<Remove generate_primes.exe>>=
```Makefile
clean: generate_primes.exe
	rm generate_primes.exe
```

@ Again, let me define `clean_win` so that people using Windows are also not left untidy!  

<<Remove generate_primes.exe>>=
```Makefile
clean_win: generate_primes.exe
	del generate_primes.exe
```

@@ I feel that the literate representation of the prime generating program is less *hostile* to a beginner
than the traditional approach. As can be seen, each chunk of the program was in its module, and each module
has got a number. I tackled the problem by writing the program from its core (<<Generate n prime numbers>>)
and later on added the lines (<<Read n from command-line>>) which would allow the user to interact with this
core. I even ended up extending a chunk (<<Include libraries>>) while I gave my reason for extending it.  

I do not know whether this convinces the reader of the beauty of literate programming, but I hope that it
does. For if programming was taught this way, I think that several of my friends won't be scared of
programming, being put off by statements after statements with comments spread out like water droplets on an
oily surface.  


## How is LitCode different from pre-existing literate programming tools?
Pre-existing literate programming tools, like WEB and CWEB, are tied to using \TeX for markup and can only
work with Pascal and C, respectively. While preventing a person from being put-off by *pure code*, I do not
want them to be put-off by the steep learning curve of \TeX/\LaTeX{} or wasting their enthusiasm in extending a
tool so that they can work with a programming language of their own choice. noweb was the tool using which I
tried to do literate programming. It can be extended much more easily than WEB/CWEB. It is also not tied to a
specific programming language. However, it does not seem to indent expanded chunks properly when `-L` flag is
used, something which can break Python code. Though noweb can be extended using `sed` and `awk`, I am probably
just too lazy to extend it. Or maybe I just needed an excuse to start my own project.  

Notebooks, like Mathematica or Jupyter, are literate programming tools only. Instead of modules they have
*cells*. A cell can have either prose or code but not both. They also do not have any names. I enjoyed using
these tools but at the same time I wanted something which is not tied to a web browser and has a client-server
model.  

While designing LitCode, I had the following objectives in mind:  

1. Build a tool which does not ties down anyone to using a specific markup language. If a programmer wants to
	use \LaTeX, they can use it. If they want to use markdown or RST, they can do that too.  

2. The weaving program can be extended in a *simpler manner* using *hooks* so that the prose and code can be
	beautified as the user wishes. Sort of how Emacs can be customized by using some lisp code. Oh yes, I could
	have used Org-mode, but at present it seems to be tied to Emacs only.  

**TL;DR:** I wanted LitCode to be flexible and simple.	

To achieve this, both `ltangle` and `lweave` use a *translation dictionary* to understand WEB files. This
dictionary is a JSON file containing the following keys:  

* `module-startswith`: Character(s) which marks the beginning of a module. Default value: `@`  

* `chunk-header-regex`: Regex pattern, which if satisfied by a line, marks the beginning of a chunk. Used by
  both `ltangle` and `lweave`. Default value: `(^<<)(.+)(>>=\\s*$)`  

* `chunk-continuation-header-regex`: Substitution pattern used by `lweave` when it finds that the definition
  of a chunk has been extended. Default value: `<<\\\\2>>+=`  

* `chunk-ref-regex`: Regex pattern, which if satisfied by a line, means that the line is a reference to
  another chunk. Used by `ltangle` while expanding chunks. Default value: `(^\\s*<<)(.+?)(>>\\s*$)`  

* `comment-startswith`: Character(s) which mark the start of a comment. Used by `ltangle` to comment out
  line-references. Default value: `None`  

* `comment-endswith`: Characters(s) which mark the end of a comment line. Used by `ltangle` to comment out
  line-references. Default value: `None`  

* `to-ignore-in-chunk`: List of characters which are supposed to be ignored by `ltangle` while expanding a
  chunk defintion. Default value: `[]`  

* `to-ignore-in-prose`: List of characters which are supposed to be ignored by `lweave` while weaving the WEB
  file(s). Default value: `[]`  

* `hooks`: Names of the python scripts which are to be run after woven lines have been generated by `lweave`.
  Python scripts are read in the order they are passed to `lweave` in command-line. If they are there in this
  list, they are executed else not. Lines of scripts are read and executed by using `exec`. Default value:
  `["insert_module_number", "format_ch_cr"]`	

As can be seen, most of the ways I felt I wanted to extend the capability of a literate programming tool have
been made possible with the introduction of this translation dictionary. Like I said earlier, this tool has
been created primarily to solve my problems. That's why I have used a 'dangerous' thing like `exec` which
would make many frown. If a user wishes to modify these and contribute to development of this project, they
can feel free to do so. But do not overcomplicate it so much! Sometimes, things are better when they are
simpler.	 


# Installation
To install LitCode in your system, the following requirements should be satisfied:  

1. If you only wish to install the program, you must be having Python 3.8 or above installed in your system.  

2. If you want to build the examples, you must have GCC installed in your system. Linux users can do so by
	installing `build-essentials`. Windows users can use either WSL2 or use MSYS2 environments to build and run
	the program.  

3. If you wish to weave the documentation, it is necessary that you have `texlive` and accompanying
	`texliveonfly` installed in your system. It is also necessary that you have `pandoc` also installed, as
	that will be using the `pdflatex` to generate the PDF of the documentation.  

Installation of LitCode is controlled entirely using a Makefile. Therefore, it would be better if you have
`make` and other such tools installed in your system. Windows users can use WSL to keep everything simple.  

**To install**  
```Bash
make install
```

**To test installation by building everything back**  
```Bash
make test-install
```

**To build out the documentation**  
```Bash
make documentation
```

**To generate a PDF of the documentation (requires pandoc)**  
```Bash
make pdf
```

**To clean everything**  
```Bash
make clean
```

**To uninstall LitCode from your system**  
```Bash
make uninstall
```


# Source Code of LitCode
## Common chunks
A few of the chunks are going to be used by all the programs that make up LitCode. Thanks to the power of
Literate Programming, I can define these chunks once here and then use them everywhere else.  

@@
@ The first chunk we are going to be defining is <<Import modules>>. Making LitCode was no rocket-science: the
scripts are simple and don't use a huge bunch of complicated libraries and modules.  

<<Import modules>>=
```Python
import os
import sys
```

@ Regex is going to be used a lot during tangling and weaving process. So, we will import `re` module.  

<<Import modules>>=
```Python
import re
```

@ As mentioned earlier, translation dictionaries are going to be used during tangling and weaving process to
parse the WEB files correctly. This requires that we load `json` module. `load()` defined in it will be used
for reading the dictionaries.  

<<Import modules>>=
```Python
import json
```

@@
@ Like all programs big and small, LitCode will also have a version number which will be printed everytime one
of the scripts is executed. We can put this version number in one chunk and use it from there everywhere.  

<<version>>=
```Python
version = '0.05'
```

@@
@ As we are building console-scripts, naturally we need a way to read command-line arguments. This will be
done by the function `get_cmd_args_dict()` defined in <<Read comman-line arguments and return them in a
dictionary>>. Keys/options/switches for the scripts are assumed to start with a hyphen, `-`. Command line
arguments are read and stored in a list until a key is encountered or if `sys.argv` has been exhausted. The
default key is an empty string, `''`.

<<Read command-line arguments and return them in a dictionary>>=
```Python
def get_cmd_args_dict():
	cmd_args_list = sys.argv[1:]
	cmd_args_dict = dict()
	switch_name = ''
	values = []
	for cmd_arg in cmd_args_list:
		if cmd_arg.startswith('-'):
			cmd_args_dict[switch_name] = values
			switch_name, values = '', []
			switch_name = cmd_arg
		else:
			values.append(cmd_arg)
		cmd_args_dict[switch_name] = values
	return cmd_args_dict
```

@@

## `linit.py`
@ The purpose of `linit.py` would be to write the standard translation dictionaries to filenames passed as
command-line arguments. The user may modify the values in these files as per their wish. If `linit` is invoked
again, it should NOT overwrite those files: it should skip writing them and exit gracefully. 

<<linit.py>>=
```Python
<<Import modules>>
<<Read command-line arguments and return them in a dictionary>>
<<Write translation dictionary to specified files>>
```

@ Translation dictionaries are going to be JSON files. `json.dumps()` does not tend to pretty-print list on a
single line. That's why we will have it defined as globally accessible multline string.

<<linit.py>>=
```Python
<<Translation dictionary as a multiline string>>
```

@ In a previous section, we have defined what all keys the translation dictionary will have. Now, we just need to
write it out. Care must be taken while escaping special-chars in regex expressions. Each double brace will in
the string will correspond to a single brace when the string is written to a file. Therefore, each special
character (example: `\s`) will be preceeded by 3 backslashes.  

<<Translation dictionary as a multiline string>>=
```Python
trd = '''{
	"module-startswith": "@",
	"chunk-header-regex": "(^<<)(.+)(>>=\\\\s*$)",
	"chunk-continuation-header-regex": "<<\\\\2>>+=",
	"chunk-ref-regex": "(^\\\\s*<<)(.+?)(>>\\\\s*$)",
	"comment-startswith": "",
	"comment-endswith": "",
	"to-ignore-in-chunk": ["^```.*$"],
	"to-ignore-in-prose": [],
	"hooks": ["insert_module_number", "format_ch_cr"]
}
'''
```

@ We can now start defining <<Write translation dictionary to specified files>>. The first the program will do
will be to print out the banner mentioning its name and version number.	 

<<Write translation dictionary to specified files>>=
```Python
def main():
	global trd
	<<version>>
	banner = f'LINIT {version}'
	print(banner)
```

@ Once this `sanity-check` of installation has been done, the program will now use `get_cmd_args_dict()` to
get a dictionary containing command line arguments. If, for some reason an empty dictionary is returned, we
should throw an error and exit. 

<<Write translation dictionary to specified files>>=
```Python
	cmd_args = get_cmd_args_dict()
	if not cmd_args:
		print('No command-line argument passed!')
		exit(1)
```

@ If either `-h` or `--help` option is passed, then we print out the information about `linit` and its usage.  

<<Write translation dictionary to specified files>>=
```Python
	elif ('-h' in cmd_args) or ('--help' in cmd_args):
		print(
			'Usage: linit -f [FILES]\n' +
			'Print a dictionary to be used by either ltangle or lweave when parsing WEB file(s)\n' + 
			'Options:\n' + 
			'{0:10}'.format('-f') + 
			'{0:32}'.format('Filename(s) to which the dictionary is to be written\n')
		)
```

@ If `-f` option has been passed, then get the list of filenames to which the translation dictionary is to be
written. If no names have been passed, throw an error. Before writing to files, we need to make sure that they
DO NOT EXIST, so that we do not end up overwriting already defined dictionaries. This can be done by using
`os.path.isfile(`*name of the file*`)`. Furthermore, the translation dictionary might be written to a file in
a subdirectory. linit should be able to create subdirectories to write the files properly. This can be done
with the use of `Path(`*name of the file*`).parent.mkdir(parents = True, exist_ok = True)`. For this we will
need to import `Path` from `pathlib`.  

<<Import modules>>=
```Python
from pathlib import Path
```

@ <<Write translation dictionary to specified files>>=
```Python
	elif '-f' in cmd_args:
		# Fetch the full path of the file to be written
		fname_list = cmd_args['-f']
		if not fname_list:
			print('Filename(s) have not been provided!')
			exit(1)
		for fname in fname_list:
			print(fname)
			# Check whether file exists or not
			if os.path.isfile(fname):
				print('File already exists. Skipping...')
			# If not, then proceed with writing it
			else:
				# Make the directory
				Path(fname).parent.mkdir(parents = True, exist_ok = True)
				# Write the dictionary to file
				with open(fname, 'w') as fp:
					fp.write(trd)
	else:
		print('No valid command-line argument provided!')
		exit(1)
	print('linit has done its job. Now exiting like a nice boy.')
```
@@

## `ltangle.py`
@ I personally felt that `ltangle` is the most complex part of LitCode. In general, tangling seems to be the
most complicated part of any literate programming tool. Each chunk needs to be pieced together from a bunch of
files and then the references inside it are also to be expanded. It seems a job best suited for recursion: you
can recursively keep on calling a function responsible for the expansion, in this case `expand_chunk_name()`
until there are no more valid chunk references left to be expanded.  

@ Instead of parsing the files again and again looking for a chunk with a specific name during reference
expansion, we can instead read the files sequentially, while maintaining a dictionary of chunks and the lines
contained in them. This dictionary will be called `chunk_dict`.  

@ We would also need ways of tracing a line in the tangled output to its source in a WEB file. This can be
done during the generation of `chunk_dict` when the files are being parsed. Later on, if the user wishes,
these 'traces' or 'references' to WEB files can be kept a comments by putting them in between
`comment-startswith` and `comment-endswith` characters defined in the translation dictionary.  

@ Finally, a way needs to be there to convert indentation in spaces to one in tabs and vice-versa. This would
make sure that the tangled output has uniform indentation. This would also be helpful when writing Makefiles
in a literate manner as they strictly use tabs for indentations.  

@ The overall structure of `ltangle.py` would be as follows:  

<<ltangle.py>>=
```Python
<<Import modules>>
<<Read command-line arguments and return them in a dictionary>>
<<Get a dictionary of chunk names and their content>>
<<Print out the dictionary of chunks>>
<<Expand chunk name>>
<<Handle indentation>>
<<Handle references to WEB files>>
<<Main subroutine for ltangle>>
```

@ The majority of the tangling process revolves around building a chunk dictionary and then expanding a
particular reference in it. Rest of the stuff (handling indentation and references to line numbers) is
comparatively easy.  

@ We begin with writing some program to generate `chunk_dict`. In this dictionary, every `chunk_name` is a key
and its content is the value. This content is read sequentially from the files which are passed as
command-line arguments to `ltangle.py`. We will receive the names of the files, we will read them one by one,
and make our dictionary.	

When making the dictionary, we have to detect whether we are reading a chunk or not. If we switch from prose
to code, we have to check whether the `chunk_name` exists in `chunk_dict` or not. If it exists, we need to
extract its *body* which is already there, and to it append the lines which are going to read now. If the
`chunk_name` does not exists in `chunk_dict`, then it's simply a *fresh* chunk.  

It might be possible that a programmer is not interested in exploding their program into chunks. They want to,
instead, program in a typical linear way, while writing prose. This is what I call *programming in notebook
mode*. To make ltangle handle this, we can insert a special key in `chunk_dict` *@->top_level_chunk_name*
which will be set equal to the name of the first chunk that is encountered when reading the files line by
lines.  

Also, we should not forget that there are some *artifacts* which are used in some markup languages to mark the
beginning and end of blocks of code. An example would be triple back-ticks in Markdown, ` ``` `. These need
to be ignored during the tangling process. These can be read from the translation dictionary and ignored
accordingly.  

@ The overall structure of the function `get_chunk_dict()` would be as follows:  

<<Get a dictionary of chunk names and their content>>=
```Python
def get_chunk_dict(fname_list, trd):
	# Initialize the chunk dictionary
	chunk_dict = dict()
	for fname in fname_list:
		# Initialize variables
		lno = 0
		chunk_name = None
		chunk_lines = []
		all_lines = None
		reading_chunk = False
		ignore_chunk_line = False
		# Read all lines from the file
		with open(fname, 'r') as fp:
			all_lines = fp.readlines()
		# Start analyzing the lines one by one.
		for line in all_lines:
			# Increment the line number
			lno += 1
			if reading_chunk:
				<<Switch to `prose mode` if a new module begins and save the chunk_name and body in chunk_dict>>
				<<Else keep on adding to the body of the chunk>>
			if not reading_chunk:
				<<Check whether the line is a chunk header or not and take required action>>
		# If you reach EOF while reading a chunk, save it!
		if chunk_name is not None:
			chunk_dict[chunk_name] = chunk_lines
	return chunk_dict
```

@ When we switch to prose mode and save a chunk's name and its body, we can also do a check on whether the
`@->top_level_chunk_name` is there in the dictionary or not. If it is not there, we add it. Even if we add it,
we would still need to save the `chunk_name` and `chunk_lines` constituting its body. Once saved, we have to
*reset* `chunk_name` and `chunk_dict`.  

<<Switch to `prose mode` if a new module begins and save the chunk_name and body in chunk_dict>>=
```Python
if line.startswith(trd['module-startswith']):
	reading_chunk = False
	if chunk_name is not None:
		if '@->top_level_chunk_name' not in chunk_dict:
			chunk_dict['@->top_level_chunk_name'] = chunk_name
		chunk_dict[chunk_name] = chunk_lines
		chunk_name = None
		chunk_lines = []
```

@ If while reading a `chunk_line`, the line doesn't start with `module-startswith` character defined in the
translation dictionary, then we can simply keep on adding the line to the body of the chunk, provided it is
not satisfying *any* pattern in the list `to-ignore-in-chunk`. If it matches any of those patterns, we can set
`ignore_chunk_line` and proceed with the analyzing the next line.    

<<Else keep on adding to the body of the chunk>>=
```Python
else:
	for pattern in trd['to-ignore-in-chunk']:
		if re.search(pattern, line):
			ignore_chunk_line = True
			break
		else:
			ignore_chunk_line = False
```

@ If the line is not supposed to be ignored, then we can append it to `chunk_lines`. But before adding it we
should also add a line mentioning the line number at which it can be found in the literate program file/WEB
file.  

<<Else keep on adding to the body of the chunk>>=
```Python
	if not ignore_chunk_line:
		indentation = re.search(r'(^[\t\ ]*)(?=\S.*$)', line)
		if indentation: indentation = indentation.group(0)
		else: indentation = ''
		comment_to_refer_src_lno = indentation + f'@->{lno}. in {fname}\n'
		chunk_lines.append(comment_to_refer_src_lno)
		chunk_lines.append(line)
```

@ There are on of the two things that can happen in a literate program:  

1. You are reading prose and you encounter a chunk-header. In that case you have to set `reading_chunk` to
   `True`. When in the next iteration the next line in the file is read, the line will be considered as a part
   of chunk and that would be it.  

2. You are reading a chunk and you encounter a `module-startswith` character. You have to set `reading_chunk`
   to False and save the current `chunk_name` and `chunk_lines` in `chunk_dict`. Now, you will need to check
   whether the same line contains a chunk-header or not. If it does, then set `reading_chunk` to `True`, else
   you can set `reading_check` to `False` and carry on with skipping all the prose.  

This explains why in `get_chunk_dict()` `if reading_chunk` comes first followed by `if not reading_chunk`
instead of `elif not reading_chunk`: the start of a module might also mark the start of a new chunk. The
converse is not true: the start of a new chunk cannot mark the start of a new module as there is supposed to
be only code in a chunk, and modules are used to define the overall structure of a literate program.  

With this exposition, we can finally write up the body of the chunk <<Check whether the line is a chunk header
or not and take required action>>  

<<Check whether the line is a chunk header or not and take required action>>=
```Python
tmp_line = line.lstrip(trd['module-startswith'])
tmp_line = tmp_line.lstrip()
chunk_name = re.search(trd['chunk-header-regex'], tmp_line)
if chunk_name:
	print(chunk_name)
	reading_chunk = True
	chunk_name = chunk_name.group(2)
	if chunk_name in chunk_dict:
		chunk_lines = chunk_dict[chunk_name]
else:
	reading_chunk = False
```

@ If no output file has been specified, `ltangle` should print out the expanded chunk and `chunk_dict`.
Printing out the expansion of a chunk is easy: we can simply join the lines and print them on the screen. To
print `chunk_dict`, we can write a function `print_chunk_dict` which would print the dictionary in a somewhat
beautiful manner.  

<<Print out the dictionary of chunks>>=
```Python
def print_chunk_dict(chunk_dict):	
	print('-' * 110)
	print('Printing chunk_dict')
	print('-' * 110)
	print('-' * 110)
	for chunk_name in chunk_dict:
		all_lines = chunk_dict[chunk_name]
		all_lines = ''.join(all_lines)
		print(f'<<{chunk_name}>>=')
		print(all_lines)
		print('-' * 110)
```

@ We have defined how a dictionary of chunks is to be generated. We now have to deal with expanding a
particular chunk name. Intuitively, it seems to be a task best suited for recursion. Here is a rough algorithm
of how a chunk name has to be expanded:  

1. Get the name of the chunk name to be expanded, `chunk_name`. See if it belongs in `chunk_dict` or not. If
   it does not, throw an error and exit program. If it exists, store the lines making up the body of the chunk
   from `chunk_dict`.  

2. Initialize an empty list, `tangled_lines`, which will hold the lines forming the body of the chunk.  

3. Go through each line in `chunk_lines` one by one:
   - If it matches `chunk-ref-regex` defined in the translation dictionary, then extract the name of the chunk
   which is being referred to, and pass it `expand_chunk_name()` to expand it. Recursion!  

   - Once you get the expansion of chunk being referred, append it to `tangled_lines` while making sure that
   all the lines in the expansion are indented with the same whitespaces with which the chunk-reference was
   indented.  

   - If the the line is not matching `chunk-ref-regex`, simply append it to `tangled_lines`.  

4. Once all the `chunk_lines` have been analyzed, simply return `tangled_lines`.  

<<Expand chunk name>>=
```Python
def expand_chunk_name(chunk_name, trd, chunk_dict):
	tangled_lines = []
	# Just check before-hand whether chunk_name exists or not
	if chunk_name in chunk_dict: chunk_lines = chunk_dict[chunk_name]
	else: 
		print(f'FATAL ERROR! {chunk_name} is not defined in the file(s) passed as command-line arguments!\a')
		exit(1)
	for line in chunk_lines:
		# Store the indentation
		indentation = re.search(r'(^[\t\ ]*)(?=\S.*$)', line)
		if indentation: indentation = indentation.group(0)
		else: indentation = ''
		# if you encounter a line matching the chunk-ref-regex, then extract the reference->chunk_name, 
		# and call expand_chunk_name again. 
		chunk_name = re.search(trd['chunk-ref-regex'], line.strip())
		if chunk_name:
			chunk_name = chunk_name.group(2)
			reference_expansion = expand_chunk_name(chunk_name, trd, chunk_dict)
			# Process reference_expansion by adding the indentation of parent to it, and add it to the tangled
			# output 
			tangled_lines += [indentation + child_line for child_line in reference_expansion]
		else:
			tangled_lines.append(line)
	return tangled_lines
```

@ Handling references to WEB files would be easy. If `-L` option has been passed in the command-line when
invoking `ltangle`, then the references to line numbers of WEB files we added when making `chunk_dict` are to
be included, else not.  

<<Handle references to WEB files>>=
```Python
def src_line_identifier_handler(tangled_lines, trd, include_comments):
	buffer = []
	for line in tangled_lines:
		tmp_line = line.lstrip()
		if tmp_line.startswith('@->') and include_comments is True:
			line = line.replace('@->', trd['comment-startswith'] + ' ')
			line = line.replace('\n', ' ' + trd['comment-endswith'] + '\n')
		elif tmp_line.startswith('@->') and include_comments is False:
			continue
		buffer.append(line)
	tangled_lines = buffer
	return tangled_lines
```

@ Conversion of tabs to spaces and vice-versa is also pretty simple. We simply need to replace a given bunch
of whitespaces to another bunch of whitespaces using `replace()` method for `str` datatype in Python. By
default, `ltangle` converts tabs to spaces. The default value of tab size is 4. To convert spaces to tabs
(important if you are building a Makefile as a literate program), then you have to invoke `ltangle` with `-t`
flag.  

<<Handle indentation>>=
```Python
def indentation_handler(tangled_lines, use_tabs, tab_size):
	buffer = []
	for line in tangled_lines:
		if use_tabs:
			line = line.replace(' ' * tab_size, '\t')
		else:
			line = line.replace('\t', ' ' * tab_size)
		buffer.append(line)
	tangled_lines = buffer
	return tangled_lines
```

@ The main subroutine will be responsible for processing command-line args passed to `ltangle` and then, based
on these arguments, generate some output, which could be a helpful listing of switches to be used with
`ltangle`, or the tangled output. The overall structure of <<Main subroutine for ltangle>> is as follows:  

<<Main subroutine for ltangle>>=
```Python
def main():
	<<version>>
	banner = 'LTANGLE ' + version
	print(banner)
	cmd_args = get_cmd_args_dict()
	fname_list = []
	ofname_list = None
	trd_fname = None
	trd = None
	chunk_name = None
	debug_mode = False
	include_comments = False
	use_tabs = False
	tab_size = 4
	tangled_lines = None
	buffer = None
	# Validate the command-line arguments that have been passed.
	# Ascertain whether any arguments have been passed or not
	if not cmd_args:
		print('No arguments have been passed!')
		exit(1)
	# It the user wishes to get some help, then he shall have it and nothing more!
	elif ('-h' in cmd_args) or ('--help' in cmd_args):
		<<Print purpose of ltangle and switches which can be used with it>>
	elif '' in cmd_args:
		<<Process command-line arguments passed to ltangle if not running in help mode>>
	else:
		print('No filename(s) have been provided!')
		exit(1)
	# Command-line arguments have been parsed. We no longer need to be in darkness of infinite nesting
	# Get a dictionary of chunks.
	chunk_dict = get_chunk_dict(fname_list, trd)
	# If no chunk name has been provided, get top_level_chunk_name from chunk_dict
	if chunk_name == '*':
		chunk_name = chunk_dict['@->top_level_chunk_name']
	# Get the tangled output.
	print(f'Calling expand_chunk_name to expand \'{chunk_name}\'')
	tangled_lines = expand_chunk_name(chunk_name, trd, chunk_dict)
	# Properly format comment lines using translation dictionary
	tangled_lines = src_line_identifier_handler(tangled_lines, trd, include_comments)
	# Convert tabs to spaces or vice-versa, as required. 
	tangled_lines = indentation_handler(tangled_lines, use_tabs, tab_size)
	# Time to print the tangled output
	tangled_lines = ''.join(tangled_lines)
	if debug_mode:
		print_chunk_dict(chunk_dict)
		print('-' * 110)
		print(f'Expansion of {chunk_name}')
		print('-' * 110)
		print(tangled_lines)
	else:
		for ofname in ofname_list:
			print(f'Attempting to write to {ofname}')
			# Make the directory
			Path(ofname).parent.mkdir(parents = True, exist_ok = True)
			# Write the dictionary to file
			with open(ofname, 'w') as fp:
				fp.write(tangled_lines)
			print(f'{ofname} written.')
	print('ltangle has done its job. Now going away like a good girl.')
```

@ I have not explained the how the command-line arguments are being processed as much of the code doing that
job is self explainatory and *boring*: just setting some switches and all. Maybe I will add a few lines
explaining them later on.  

Still, the big picture is that if `-h` or `--help` option is passed to `ltangle`, then it will run in `help`
mode irrespective of whatever other arguments have been passed to it. If it is not running in help-mode, then
it will tangle the chunk-name out of the list of WEB files passed to it as argument.  

@ <<Print purpose of ltangle and switches which can be used with it>>=
```Python
print(
	'Usage: ltangle [FILES] -trd [FILE[.json]] [OPTIONS]\n' +
	'Extract a chunk from the WEB files using a translation dictionary\n' + 
	'Options:\n' + 
	'{0:10}'.format('-trd') + 
	'{0:32}'.format('Name of the translation dictionary to be used while tangling the file\n') +
	'{0:10}'.format('-c') + 
	'{0:32}'.format('Name of the chunk to be expanded. If not provided, contents of the first \n') +
	'{0:10}'.format('') + 
	'{0:32}'.format('chunk encountered are expanded.\n') +
	'{0:10}'.format('-o') + 
	'{0:32}'.format('Files to which the tangled source code is to be written. If none are \n') +
	'{0:10}'.format('') + 
	'{0:32}'.format('provided then ltangle will print the tangled code on the screen.\n') +
	'{0:10}'.format('-L') +
	'{0:32}'.format('Add line numbers as comments in the tangled code identifying the source\n') +
	'{0:10}'.format('') + 
	'{0:32}'.format('of the line following it.') +
	'{0:10}'.format('\n-t') +
	'{0:32}'.format(' Use tabs for indentations; n spaces are converted to tabs. By default, \n') + 
	'{0:10}'.format('') +
	'{0:32}'.format('spaces are used for indentation. If n is not provided, it is set to 4.\n')
)
exit(0)
```

@ <<Process command-line arguments passed to ltangle if not running in help mode>>=
```Python
# Get file-names
fname_list = cmd_args['']
# Check if the fname_list is empty
if not fname_list:
	print('No filename(s) have been provided!')
	exit(1)
# Load the translation dictionary, else throw an error if it has not be provided
if '-trd' in cmd_args:
	trd_fname = cmd_args['-trd'][0]
	trd = json.load(open(trd_fname, 'r'))
else:
	print('Translation dictionary to be used during tangling has not been specified!\n')
	exit(1)
# See if the chunk_name to be expanded is provided or not. Else work in notebook mode. 
if '-c' in cmd_args:
	chunk_name = cmd_args['-c']
	if chunk_name:
		chunk_name = chunk_name[0]
	else:
		chunk_name = '*'
else:
	chunk_name = '*'
if chunk_name == '*':
	print('No chunk name has been provided. ltangle will expand the first chunk it encounters.')
# Load the name of the files to which the tangled output is to be written, else enter debugging mode
# and print the translation dictionary and tangled output on the screen
if '-o' in cmd_args:
	ofname_list = cmd_args['-o']
if '-o' not in cmd_args or ofname_list == []:
	debug_mode = True
	print('No output files have been specified!\nTangled output will be printed on the screen.')
else:
	debug_mode = False
# Of course this means that you can `hack' ltangle by running it with -R *
# Set include_comments = True if -L option is passed
if '-L' in cmd_args:
	include_comments = True
# Set use_tabs to True if -t option is passed. By default, 4 spaces = 1 Tab 
if '-t' in cmd_args:
	use_tabs = True
	if cmd_args['-t']:
		tab_size = int(cmd_args['-t'][0])
	else:
		print('Tabsize not provided! 4 will be used.')
		tab_size = 4
```

@@

## `lweave.py`
@ We stand on the shoulders of the giants. Much of the key ideas and chunks have already been explained in
`linit.py` and `ltangle.py`. Writing `lweave.py`, the program responsible for weaving, is cakewalk compared to
them. The overall structure of `lweave.py` is simple:

<<lweave.py>>=
```Python
<<Import modules>>

trd = None
woven_lines = None

<<Read command-line arguments and return them in a dictionary>>
<<Generate woven lines>>
<<Main subroutine for lweave>>
```

@ One thing which the reader will straightaway notice is that unlike in `ltangle`, both `trd` and the list
holding the processed lines, `woven_lines`, are defined as global variables. This is because we will be using
`exec()` to execute Python code present in strings to further process `woven_lines`. It is much easier to set
them as global variables and process `woven_lines` further in `exec()`.  

@ The key processing tasks that `lweave.py` does to generate *beautified* documents are:  

1. Ignore the lines present in the list `to-ignore-in-prose` defined in the translation dictionary.  

2. If a chunk-name has already been defined in the literate program, replace the header with
   `chunk-continuation-header-regex` defined in the translation dictionary. This can be done by keeping a
   track of chunk-names by storing them in a list. If a chunk-name is already there in the list, then its body
   is a continuation of the definition of the chunk. To denote this continuation, we can use `re.sub()` to
   change the way the header is written. Else if it is not in the list, it is a new chunk and we do not have
   to perform any substitutions.  

<<Generate woven lines>>=
```Python
def get_woven_lines(fname_list, trd):
	chunk_name = None
	chunk_name_list = []
	woven_lines = []
	for fname in fname_list:
		lines = None
		reading_chunk = False
		with open(fname, 'r') as fp:
			lines = fp.readlines()
		print(fname)
		for line in lines:
			if trd['to-ignore-in-prose']:
				if re.search(trd['to-ignore-in-prose'], line):
					continue
			tmp_line = line.lstrip(trd['module-startswith'])
			tmp_line = tmp_line.lstrip()
			chunk_name = re.search(trd['chunk-header-regex'], tmp_line)
			if chunk_name:
				print(chunk_name)
				chunk_name = chunk_name.group(2)
				if chunk_name not in chunk_name_list:
					chunk_name_list.append(chunk_name)
				else:
					line = re.sub(trd['chunk-header-regex'], trd['chunk-continuation-header-regex'], line)
					line += '\n'
			woven_lines.append(line)
	return woven_lines
```

@ <<Main subroutine for lweave>>=
```Python
def main():
	global trd, woven_lines
	banner = 'LWEAVE 0.2.203 (bootstrap version)'
	print(banner)
	cmd_args = None
	fname_list = []
	ofname_list = []
	trd_fname = None
	debug_mode = False
	hook_list = []
	hook_lines = None
	# Get dictionary of command-line arguments
	cmd_args = get_cmd_args_dict()
	# Process these command-line arguments
	if not cmd_args:
		print('No arguments have been passed!')
		exit(1)
	elif ('-h' in cmd_args) or ('--help' in cmd_args):
		<<Print purpose of lweave and switches which can be used with it>>
	elif '' in cmd_args:
		<<Process command-line arguments passed to lweave if not running in help mode>>
	else:
		print('No filename(s) have been provided!')
		exit(1)
	# Generate woven lines
	woven_lines = get_woven_lines(fname_list, trd)
	<<Execute hooks>>
	# Write the woven output to the files if debug_mode = False, else print it on the screen
	woven_lines = ''.join(woven_lines)
	if debug_mode:
		print('-' * 110)
		print(f'Woven output')
		print('-' * 110)
		print(woven_lines)
	else:
		for ofname in ofname_list:
			print(f'Attempting to write to {ofname}')
			# Make the directory
			Path(ofname).parent.mkdir(parents = True, exist_ok = True)
			# Write the dictionary to file
			with open(ofname, 'w') as fp:
				fp.write(woven_lines)
			print(f'{ofname} written.')
	print('lweave has done its job. Consider it a gift from God!')
```

@ <<Print purpose of lweave and switches which can be used with it>>=
```Python
print(
	'Usage: lweave [FILES] -trd [FILE[.json]] [OPTIONS]\n' +
	'Weave a beautiful document containing the content of WEB files' + 
	'using a translation dictionary\n' + 
	'Options:\n' + 
	'{0:10}'.format('-trd') + 
	'{0:32}'.format('Name of the translation dictionary to be used while weaving the files.\n') +
	'{0:10}'.format('-hk') + 
	'{0:32}'.format('Name of the hooks to be executed after preprocessing the content of \n') + 
	'{0:10}'.format('') +
	'{0:32}'.format('WEB files. Hooks are executed in the order they are presented\n') +
	'{0:10}'.format('-o') +
	'{0:32}'.format('Files to which the woven prose is to be written.\n')
)
exit(0)
```

@ <<Process command-line arguments passed to lweave if not running in help mode>>=
```Python
# Get file-names
fname_list = cmd_args['']
# Check if the fname_list is empty
if not fname_list:
	print('No filename(s) have been provided!')
	exit(1)
# Load the translation dictionary, else throw an error if it has not be provided
if '-trd' in cmd_args:
	trd_fname = cmd_args['-trd'][0]
	trd = json.load(open(trd_fname, 'r'))
else:
	print('Translation dictionary to be used during weaving has not been specified!\n')
	exit(1)
# Load the name of the files to which the woven output is to be written, else
# print it on the screen
if '-o' in cmd_args:
	ofname_list = cmd_args['-o']
if '-o' not in cmd_args or ofname_list == []:
	debug_mode = True
	print('No output files have been specified!\nWoven output will be printed on the screen.')
# Load the names of the hooks that have been provided. If none are specified, then no hooks will be
# executed by default
if '-hk' in cmd_args:
	hook_list = cmd_args['-hk']
```

@ Process the lines further by executing the scripts present in the list `hooks` in the translation
dictionary. At the end of each of these hooks, it is important to make sure that `woven_lines` is set so that
the modifications made when executing the hooks really take affect.  

<<Execute hooks>>=
```Python
for hook in hook_list:
	if hook in trd["hooks"]:
		with open(hook, 'r') as fp:
			hook_lines = fp.readlines()
		hook_lines = ''.join(hook_lines)
		print(f'Executing hook: {hook}')
		exec(hook_lines, globals())
```

@@
### Examples of hooks
At this point I would like to give the reader two examples of hooks which will be used very often:
`insert_module_number` and `format_ch_cr`. While the former will be used to insert a number instead of
`module-startswith` character, the latter will be used to format chunk-headers and references using control
words defined in \TeX{}.  

**`format_ch_cr`**  

@ <<format_ch_cr>>=
```Python
buffer = []
reading_chunk = False
for line in woven_lines:
	if reading_chunk:
		if line.startswith(trd['module-startswith']):
			reading_chunk = False
		else:
			is_chunk_reference = re.search(trd['chunk-ref-regex'], line)
			if is_chunk_reference:
```

@ If we encounter a chunk-reference inside a chunk, then it is best to comment it out. That is the simplest
and least problematic way to make them look beautiful in the woven document.  

<<format_ch_cr>>= 
```Python
				line = line.replace('<<', trd['comment-startswith'] + '<<')
				line = line.replace('>>', '>>' + trd['comment-endswith'])
	if not reading_chunk:
		tmp_line = line.lstrip(trd['module-startswith'])
		tmp_line = tmp_line.lstrip()
		is_chunk_header = re.search(trd['chunk-header-regex'], tmp_line)
		if is_chunk_header:
			reading_chunk = True
			line = line.replace('<<', '$\\\\langle$*')
			line = line.replace('>>=', '*$\\\\rangle\\\\!\\\\!\\\\equiv$')
		else:
			is_chunk_header = re.search(r'(^<<)(.+)(>>\+=\s*$)', tmp_line)
			if is_chunk_header:
				reading_chunk = True
				line = line.replace('<<', '$\\\\langle$*')
				line = line.replace('>>+=', '*$\\\\rangle+\\\\!\\\\!\\\\equiv$')
			else:
				reading_chunk = False
				line = line.replace('<<', '$\\\\langle$*')
				line = line.replace('>>', '*$\\\\rangle$')
	buffer.append(line)
woven_lines = buffer
```

@@

**`insert_module_number`**  

@ Inserting module numbers is simple: simply replace `module-startswith` character with the value in the
counter and increment the counter.  

<<insert_module_number>>=
```Python
count = 0
buffer = []
for line in woven_lines:
	if line.startswith(trd['module-startswith']):
		if line[1] != trd['module-startswith']:	
			count += 1
			print(count)
			line = '**' + str(count) + '.**  ' + line[1:]
		else:
			print('Skipping and resetting!')
			count = 0
			line = line[2:]
	buffer.append(line)
woven_lines = buffer
```

@@

## `lhooks.py`
@ A user of LitCode might not be interested in copy-pasting `format_ch_cr` and `insert_module_number` everytime
they write a literate program. So, it is best to have a script which does this job for them. Just run `lhooks`
and it will write the helpful hooks in the current directory. It will skip writing the hooks if they already
exist.  

<<lhooks.py>>=
```Python
<<Import modules>>

format_ch_cr = '''
<<format_ch_cr>>
'''

insert_module_number = '''
<<insert_module_number>>
'''

def main():
	global format_ch_cr, insert_module_number
	if not os.path.isfile('format_ch_cr'):
		with open('format_ch_cr', 'w') as fp:
			fp.write(format_ch_cr)
	else:
		print('Skipping writing format_ch_cr')
	if not os.path.isfile('insert_module_number'):
		with open('insert_module_number', 'w') as fp:
			fp.write(insert_module_number)
	else:
		print('Skipping writing insert_module_number')
```

@@
## `__init__.py` and `setup.py`
We will be using the scripts we have defined so far as console-scripts. We can install them in a system in
two ways:  

**A.** Put a shebang line at the top of each script which tells the location of the Python runtime. Theses
scripts need to be set as executables, something which can be done by using `chmod +x`. We also need to
include their path in `PATH` variable so that the shell can know where they are. The first few versions of
LitCode were installed this way only.  

**B.** Use `pip` and `setuptools` to install the package as a console scripts.  

Option B is much more cleaner and we are going to install LitCode using it. For this we need to have
`__init__.py` and `setup.py`.  

First, some exposition (copied verabitm from StackOverflow):  

* Package - A folder/directory that contains `__init__.py` file.  
  
* Module - A valid python file with .py extension.  
  
* Distribution - How one package relates to other packages and modules.

First let us get `__init__.py` out of the way. It is basically a *special* blank file which tells Python that
the directory in which it resides is a package.  

<<__init__.py>>=
```Python

```

@@

The purpose of `setup.py` is to ensure that the package is distributed and installed properly across various
systems while taking care of dependencies.  

<<setup.py>>=
```Python
from setuptools import setup, find_packages

<<version>>
setup(
	name = 'litcode',
	version = version,
	packages = find_packages(),
	entry_points = {
		'console_scripts' : [
			'linit=litcode.linit:main',
			'ltangle=litcode.ltangle:main',
			'lweave=litcode.lweave:main',
			'lhooks=litcode.lhooks:main'
		]
	}
)
```

@@
Using these scripts, we can use `pip` to install LitCode in a system.  

