.PHONY: all clean

all: $(wildcard *.tex) $(wildcard *.sty) $(wildcard *.bib)
	pdflatex litcode.tex
	biber litcode
	pdflatex litcode.tex
	pdflatex litcode.tex

clean: $(wildcard *.aux) $(wildcard *.log) $(wildcard *.lol) $(wildcard *.out) $(wildcard *.toc) \
	$(wildcard *.gz) $(wildcard *.bbl) $(wildcard *.bcf) $(wildcard *.blg) $(wildcard *.xml)
	rm $^