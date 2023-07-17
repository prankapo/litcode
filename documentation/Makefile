.PHONY: all clean

all: $(wildcard *.tex) $(wildcard *.sty) $(wildcard *.bib)
	texliveonfly litcode.tex
	pdflatex litcode.tex
	bibtex litcode.aux
	pdflatex litcode.tex
	pdflatex litcode.tex

clean: $(wildcard *.aux) $(wildcard *.log) $(wildcard *.lol) $(wildcard *.out) $(wildcard *.toc) \
	$(wildcard *.gz)
	rm $^