LitCode v0.10 - Markup language agnostic implementation of LitCode  

- Modified: ./  
        * Description: LitCode root directory  
        * Deleted: fix_4_gfm: lweave is no longer using hooks to extend its functionality.  
        * Deleted: format_ch_cr  
        * Deleted: insert_module_number  
        * Modified: Makefile: Solves the chicken and egg problem by building LitCode using boostrap code, followed by 
        installing and testing it.  
        * Modified: setup.py: New version number.  

- Deleted: bootstrap  
        * Description: Bootstrap code for building LitCode from its WEB files. LitCode is no longer implemented as a 
        literate program to ease up testing a bit (otherwise there were a lot of chicken-and-egg-problems).

- New: litcode  
        * Description: Contains the source code of LitCode. LitCode v0.10 is markup agnostic and is able to:
        A. Read chunk names continuining on next line due to hard wraps  
        B. 'Autocomplete' chunk names ending with triple dots `...`. This saves programmers time by not having them to 
        type long chunk names again and again.  
        C. LitCode is no longer completely reliant on regular expressions to parse a literate program. A programmer can 
        either use the default markup table for literate programs (which allows chunk definition to be written in 
        Markdown code blocks), or modify it easily by replacing values of required keys as they wish.  
        * New: linit.py: Responsible for writing default literate markup table (used for processing literate programs by 
        ltangle and lweave) and markup tables for markdown, Restructured text, LaTeX and plain text (used by lweave to 
        properly format literate program in a given markup language).  
        * New: litcore.py: Contains implementation of LitCode lexer, as well as important function for reading 
        command-line arguments, chunk names, etc.  
        * New: ltangle.py: Responsible for tangling out source code from a literate program file.  
        * New: lweave.py: Responsible for weaving a documentation by 'reading' literate program file using literate 
        markup table and inserting characters/strings in markup table (for a markup language).  

- Deleted: figures  
        * Description: No figure has been included in README file.  

- Deleted: web  
        * Description: LitCode v0.10 has not been implemented as a literate program so as to:  
        1. Allow for fast testing and debugging.  
        2. Prevent chicken-and-egg problems encountered when a language interpreter is being defined in its own 
        language. 
