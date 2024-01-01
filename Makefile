BOOT := bootstrap
DOC := documentation
EXAMPLES := examples
WEB := web
SHELL := /usr/bin/bash

.PHONY: all clean boot src install examples documentation buildtex

all:
	@echo "Performing initial tangling of web files using bootstrap code..."
	$(MAKE) tangle
	@echo "Done.\n"
	@echo "Installing using pip..."
	$(MAKE) install
	@echo "Done.\n"
	@echo "Clearing the directories..."
	$(MAKE) clean
	@echo "Done.\n"
	@echo "Tangling using installed scripts..."
	$(MAKE) tangle
	@echo "Done.\n"
	@echo "Weaving using installed scripts..."
	$(MAKE) weave
	@echo "Done.\n"
	@echo "Building the documentation..."
	-$(MAKE) buildtex
	@echo "Done.\n"
	@echo "Running the examples for your satisfaction..."
	$(MAKE) runex
	@echo "Done.\n"

# This part is for generating the 'raw' source files
tangle: web/source_code.web src examples

# club_web: Clubs serveral web files containing the source code into a single file named source_code.web
web/source_code.web: web/styling_file.web web/linit.web web/ltangle.web web/lweave.web web/setup.web
	cd web && \
	echo -e "\\section{Source Code}\n" > source_code.web && \
	cat styling_file.web \
	    linit.web \
	    ldump.web \
	    ltangle.web \
	    lweave.web \
	    setup.web \
	    >> source_code.web
	-echo "Clubbing done."

src: $(wildcard web/*.web) web/source_code.web
	mkdir -p litcode
	python3 $(BOOT)/ldump.py $(WEB)/source_code.web > $(WEB)/src.json
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R setup.py > setup.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R __init__.py > litcode/__init__.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R linit.py > litcode/linit.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R ldump.py > litcode/ldump.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R ltangle.py > litcode/ltangle.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R lweave.py > litcode/lweave.py

examples: $(wildcard web/*.web) web/source_code.web
	mkdir -p examples
	python3 $(BOOT)/ldump.py web/examples.web > web/examples.json
	python3 $(BOOT)/ltangle.py -i web/examples.json -R fibonacci.c -cc '//' > examples/fibonacci.c
	python3 $(BOOT)/ltangle.py -i web/examples.json -R primes.c -cc '//' > examples/primes.c
	python3 $(BOOT)/ltangle.py -i web/examples.json -R Makefile -cc '#' -ut 4 > examples/Makefile

install: $(wildcard litcode/*.py)
	python3 -m pip install .

# weave: weaving the documentation
weave: documentation buildtex

documentation: $(wildcard web/*.web) web/source_code.web
	mkdir -p documentation
	linit $(DOC)
	lweave web/litcode.web > documentation/litcode.tex
	lweave web/introduction.web web/source_code.web web/examples.web > $(DOC)/content.tex 
	cp web/references.web $(DOC)/references.bib

# buildtex: compile the PDF
buildtex: $(DOC)/litcode.tex $(DOC)/references.bib
	@echo "Building using LaTeX"
	-cd documentation && \
	texliveonfly litcode.tex
	-cd documentation && \
	biber litcode && \
	pdflatex litcode.tex && \
	pdflatex litcode.tex && \
	pdf2htmlEX litcode.pdf --zoom 2
	@echo "Done.\n"

# buildtex: compile the PDF
buildtex-fast: $(DOC)/litcode.tex $(DOC)/references.bib
	@echo "Building using LaTeX"
	-cd documentation && \
	texliveonfly litcode.tex
	-cd documentation && \
	biber litcode && \
	pdflatex -interaction=batchmode litcode.tex && \
	pdflatex -interaction=batchmode litcode.tex && \
	pdf2htmlEX litcode.pdf --zoom 2 --process-outline 
	@echo "Done.\n"
	
# runex: Run the examples
runex: $(wildcard examples/*.c) examples/Makefile
	(cd examples;make runfib; make runprimes)

# clean: cleans everything except for web files
clean:
	-rm web/*.json 
	-rm web/source_code.web
	-rm -rf litcode setup.py examples documentation
	-rm -rf litcode.egg-info
	-rm -rf build

# uninstall: uninstalls the scripts
uninstall: 
	echo 'Uninstalling LitCode'
	python3 -m pip uninstall litcode
	echo 'LitCode uninstalled successfully'