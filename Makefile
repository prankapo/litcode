BOOT := bootstrap
DOC := documentation
EXAMPLES := examples
WEB := web
SHELL := /usr/bin/bash

.PHONY: all clean boot src install examples documentation buildtex

all:
	@echo "Performing initial tangling of web files using bootstrap code..."
	$(MAKE) boot
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
	@echo "Done.\n"

# This part is for generating the 'raw' source files
boot: 
	mkdir -p litcode
	python3 $(BOOT)/ldump.py $(WEB)/setup.web > $(WEB)/src.json
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R setup.py > setup.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R __init__.py > litcode/__init__.py
	python3 $(BOOT)/ldump.py $(WEB)/plsty.web $(WEB)/styling_file.web > $(WEB)/src.json
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R plsty.py > litcode/plsty.py
	python3 $(BOOT)/ldump.py $(WEB)/ldump.web $(WEB)/ltangle.web $(WEB)/lweave.web > $(WEB)/src.json
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R ldump.py > litcode/ldump.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R ltangle.py > litcode/ltangle.py
	python3 $(BOOT)/ltangle.py -i $(WEB)/src.json -R lweave.py > litcode/lweave.py

tangle: src

src:
	mkdir -p litcode
	ldump $(WEB)/setup.web > $(WEB)/src.json
	ltangle -i $(WEB)/src.json -R setup.py > setup.py
	ltangle -i $(WEB)/src.json -R __init__.py > litcode/__init__.py
	ldump $(WEB)/plsty.web $(WEB)/styling_file.web > $(WEB)/src.json
	ltangle -i $(WEB)/src.json -R plsty.py > litcode/plsty.py
	ldump $(WEB)/ldump.web $(WEB)/ltangle.web $(WEB)/lweave.web > $(WEB)/src.json
	ltangle -i $(WEB)/src.json -R ldump.py > litcode/ldump.py
	ltangle -i $(WEB)/src.json -R ltangle.py > litcode/ltangle.py
	ltangle -i $(WEB)/src.json -R lweave.py > litcode/lweave.py

install: $(wildcard litcode/*.py)
	python3 -m pip install .

# weave: weaving the documentation
weave: documentation buildtex

documentation: $(wildcard web/*.web)
	mkdir -p documentation
	plsty $(DOC)
	lweave $(WEB)/litcode.web > $(DOC)/litcode.tex
	lweave $(WEB)/introduction.web > $(DOC)/introduction.tex
	lweave $(WEB)/ldump.web > $(DOC)/ldump.tex
	lweave $(WEB)/ltangle.web > $(DOC)/ltangle.tex
	lweave $(WEB)/lweave.web > $(DOC)/lweave.tex
	lweave $(WEB)/styling_file.web > $(DOC)/styling_file.tex
	lweave $(WEB)/plsty.web > $(DOC)/plsty.tex
	lweave $(WEB)/setup.web > $(DOC)/setup.tex
	cp web/references.web $(DOC)/references.bib

# buildtex: compile the PDF
buildtex: $(DOC)/litcode.tex $(DOC)/references.bib
	@echo "Building using LaTeX"
	-cd documentation && \
	texliveonfly litcode.tex
	-cd documentation && \
	biber litcode && \
	pdflatex litcode.tex && \
	pdflatex litcode.tex
	@echo "Done.\n"

# buildtex: compile the PDF
buildtex-fast: $(DOC)/litcode.tex $(DOC)/references.bib
	@echo "Building using LaTeX"
	-cd documentation && \
	texliveonfly litcode.tex
	-cd documentation && \
	biber litcode && \
	pdflatex -interaction=batchmode litcode.tex && \
	pdflatex -interaction=batchmode litcode.tex
	@echo "Done.\n"

# clean: cleans everything except for web files
clean:
	-rm web/*.json 
	-rm web/source_code.web
	-rm -rf litcode setup.py
	-find documentation/ ! -name 'litcode.pdf' -type f -exec rm -f {} +
	-rm -rf litcode.egg-info
	-rm -rf build

# uninstall: uninstalls the scripts
uninstall: 
	echo 'Uninstalling LitCode'
	python3 -m pip uninstall litcode
	echo 'LitCode uninstalled successfully'