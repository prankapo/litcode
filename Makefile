.PHONY: dummy install tests uninstall clean

dummy:
	echo "No target provided, so nothing will be cooked!"

install:
	python3 -m pip install . 

install-win:
	python -m pip install .

install-darwin:
	python3 -m pip install . --break-system-packages

tests:
	cp -v litcode/litcore.py tests/litcore.py
	cp -v litcode/linit.py tests/linit.py
	cp -v litcode/ltangle.py tests/ltangle.py
	cp -v litcode/lweave.py tests/lweave.py
	printf "\nmain()\n" >> tests/linit.py
	printf "\nmain()\n" >> tests/ltangle.py
	printf "\nmain()\n" >> tests/lweave.py
	(cd tests; make tests)

tests-win:
	cp -v litcode/litcore.py tests/litcore.py
	cp -v litcode/linit.py tests/linit.py
	cp -v litcode/ltangle.py tests/ltangle.py
	cp -v litcode/lweave.py tests/lweave.py
	printf "\nmain()\n" >> tests/linit.py
	printf "\nmain()\n" >> tests/ltangle.py
	printf "\nmain()\n" >> tests/lweave.py
	(cd tests; make tests-win)

md2html:
	pandoc --standalone --from=markdown --to=html -V maxwidth=60em README.md -o README.html

clean:
	-rm -rf litcode.egg-info/ 
	-rm -rf litcode/__pycache__
	-rm -rf build
	-(cd tests/; make clean;)
	-rm README.html

uninstall: 
	python3 -m pip uninstall litcode 

uninstall-win:
	python -m pip uninstall litcode

uninstall-darwin:
	python3 -m pip uninstall litcode --break-system-packages
