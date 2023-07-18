BOOT := ./bootstrap
DOC := ./documentation
EXAMPLES := ./examples
WEB := ./web
SHELL := /usr/bin/bash

.PHONY: all clean boot src install examples documentation build buildtex buildex

all: boot src install examples documentation

boot: $(wildcard bootstrap/*)
	(cd bootstrap; source build.sh)

src: $(wildcard web/*.web)
	ldump $(WEB)/source_code.web > $(WEB)/src.json
	ltangle -i $(WEB)/src.json -R linit.py > src/linit.py
	ltangle -i $(WEB)/src.json -R ldump.py -cc '#' > src/ldump.py
	ltangle -i $(WEB)/src.json -R ltangle.py -cc '#' > src/ltangle.py
	ltangle -i $(WEB)/src.json -R lweave.py -cc '#' > src/lweave.py

install: $(wildcard src/*.py)
	-cp src/linit.py src/linit.tmp
	-cp src/ldump.py src/ldump.tmp
	-cp src/ltangle.py src/ltangle.tmp
	-cp src/lweave.py src/lweave.tmp
	-sudo chmod +x src/*.tmp;
	-sudo cp src/linit.tmp ~/local/bin/linit
	-sudo cp src/ldump.tmp ~/local/bin/ldump
	-sudo cp src/ltangle.tmp ~/local/bin/ltangle
	-sudo cp src/lweave.tmp ~/local/bin/lweave
	-rm src/*.tmp

examples: $(wildcard web/*.web)
	ldump web/examples.web > web/examples.json
	ltangle -i web/examples.json -R fibonacci.c -cc '//' > examples/fibonacci.c
	ltangle -i web/examples.json -R primes.c -cc '//' > examples/primes.c
	ltangle -i web/examples.json -R Makefile -cc '#' > examples/Makefile

documentation: $(wildcard web/*.web)
	linit $(DOC)
	lweave web/litcode.web > documentation/litcode.tex
	lweave web/introduction.web web/source_code.web web/examples.web > $(DOC)/content.tex 
	cp web/references.web $(DOC)/references.bib

build: buildtex buildex

buildtex: $(DOC)/litcode.tex $(DOC)/references.bib
	(cd documentation; make all)

buildex: $(wildcard examples/*.c) examples/Makefile
	(cd examples;make all)

clean:
	(cd documentation; make clean)
	(cd examples; make clean)

uninstall: 
	echo 'Uninstalling LitCode'
	rm -f ~/local/bin/linit ~/local/bin/ldump ~/local/bin/ltangle ~/local/bin/lweave
	echo 'LitCode ninstalled successfully'