DOC := ./documentation
SHELL := /usr/bin/bash

buildlatex: $(wildcard *.tex)
	clear;
	cd $(DOC) && texliveonfly litcode.tex .
	cd $(DOC) && pdflatex litcode.tex .
	cd $(DOC) && pdflatex litcode.tex .

clean: $(wildcard $(DOC)/*.aux) $(wildcard $(DOC)/*.log) $(wildcard $(DOC)/*.out) $(wildcard $(DOC)/*.lol)
	rm $^

tangle: src_code.tex
	notangle src_code.tex -Rlitcode.py > litcode.py

prototests: bootstrap/litcode.py
	source bootstrap/build.sh