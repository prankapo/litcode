DOC := document2.tex

build: $(wildcard *.tex) $(wildcard.sty)
	echo 'Building PDF'
	texliveonfly $(DOC)
	pdflatex $(DOC)
	pdflatex $(DOC)
	echo 'Done'
	echo 'Building HTML'
	pandoc --standalone --toc --listings --mathjax=https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML -f latex -t html $(DOC) -o result.html
	echo 'Done'

	