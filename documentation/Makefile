.PHONY: all clean

all: $(wildcard *.tex) $(wildcard *.sty) $(wildcard *.bib)
	texliveonfly litcode.tex
	biber litcode
	pdflatex litcode.tex
	pdflatex litcode.tex
	pdf2htmlEX litcode.pdf --zoom 2

clean: $(wildcard *.aux) $(wildcard *.log) $(wildcard *.lol) $(wildcard *.out) $(wildcard *.toc) \
	$(wildcard *.gz) $(wildcard *.bbl) $(wildcard *.bcf) $(wildcard *.blg) $(wildcard *.xml)
	rm $^