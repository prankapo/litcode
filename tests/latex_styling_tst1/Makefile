build: $(wildcard *.tex) $(wildcard.sty)
	echo 'Building PDF'
	texliveonfly document1.tex
	pdflatex document1.tex
	pdflatex document1.tex
	echo 'Done'
	echo 'Building HTML'
	pandoc --standalone --toc --listings --mathjax=https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML -f latex -t html document1.tex -o document1.html
	echo 'Done'

	