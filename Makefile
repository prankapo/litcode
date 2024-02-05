BOOT := bootstrap
DOC := documentation
EXAMPLES := examples
WEB := web
SHELL := /usr/bin/bash

.PHONY: install test-install boot chicken trd src hooks documentation pdf examples clean uninstall

install: 
	@echo "Installing LitCode..."
	$(MAKE) boot
	$(MAKE) chicken
	python3 -m pip install .
	@echo "Done."

test-install: 
	$(MAKE) clean
	$(MAKE) trd
	$(MAKE) trd
	$(MAKE) src
	$(MAKE) hooks
	$(MAKE) hooks
	$(MAKE) documentation

boot:
	@echo "Using bootstrap code to tangle linit and ltangle..."
	python3 bootstrap/linit.py -f trd.json
	python3 bootstrap/ltangle.py web/README.md -trd trd.json -t 4 -c linit.py -o litcode-tmp/linit.py
	python3 bootstrap/ltangle.py web/README.md -trd trd.json -t 4 -c ltangle.py -o litcode-tmp/ltangle.py
	@echo "Done."
	@echo 'Modifying linit.py and ltangle.py...'
	@echo 'main()' >> litcode-tmp/linit.py
	@echo 'main()' >> litcode-tmp/ltangle.py
	@echo "Done."

chicken:
	@echo "Using linit and ltangle to build LitCode..."
	python3 litcode-tmp/linit.py -f trd.json
	python3 litcode-tmp/ltangle.py web/README.md -trd trd.json -t 4 -c linit.py -o litcode/linit.py
	python3 litcode-tmp/ltangle.py web/README.md -trd trd.json -t 4 -c ltangle.py -o litcode/ltangle.py
	python3 litcode-tmp/ltangle.py web/README.md -trd trd.json -t 4 -c lweave.py -o litcode/lweave.py
	python3 litcode-tmp/ltangle.py web/README.md -trd trd.json -t 4 -c lhooks.py -o litcode/lhooks.py
	python3 litcode-tmp/ltangle.py web/README.md -trd trd.json -t 4 -c __init__.py -o litcode/__init__.py
	python3 litcode-tmp/ltangle.py web/README.md -trd trd.json -t 4 -c setup.py -o setup.py
	rm -rf litcode-tmp
	@echo "Done."

trd:
	linit -f trd.json
	sed -i 's/"comment-startswith":.*/"comment-startswith":"\\"",/g' trd.json
	sed -i 's/"comment-endswith":.*/"comment-endswith":"\\"",/g' trd.json
	
src:
	ltangle web/README.md -trd trd.json -t 4 -c linit.py -o litcode/linit.py
	ltangle web/README.md -trd trd.json -t 4 -c ltangle.py -o litcode/ltangle.py
	ltangle web/README.md -trd trd.json -t 4 -c lweave.py -o litcode/lweave.py
	ltangle web/README.md -trd trd.json -t 4 -c lhooks.py -o litcode/lhooks.py
	ltangle web/README.md -trd trd.json -t 4 -c __init__.py -o litcode/__init__.py
	ltangle web/README.md -trd trd.json -t 4 -c setup.py -o setup.py

hooks:
	lhooks

documentation:
	(cd figures; make literate_workflow; make clean)
	lweave web/README.md -trd trd.json -hk format_ch_cr insert_module_number fix_4_gfm -o README.md
	doctoc README.md

pdf:
	pandoc -s -r markdown -t pdf -V geometry:margin=2.5cm,landscape README.md -o README.pdf

examples:
	ltangle web/README.md -trd trd.json -c generate_primes.c -o examples/generate_primes.c
	ltangle web/README.md -trd trd.json -c make_example.mk -t 4 -o examples/Makefile
	(cd examples; make test; make clean)

clean:
	-rm -rf litcode/
	-rm -rf litcode-tmp/
	-rm -rf litcode.egg-info/
	-rm -rf build/
	-rm -rf examples/
	-rm *.pdf
	-rm setup.py

uninstall: 
	@echo "Uninstalling LitCode..."
	python3 -m pip uninstall litcode
	@echo "Done."