switch_files := crude/switch/switch1.md crude/switch/switch2.md

.PHONY: dummy tests lmt sample switch primes clean tests-win lmt-win sample-win switch-win primes-win

dummy:
	@echo "No target provided, so nothing will be cooked!"

tests: lmt sample switch primes

lmt: 
	clear
	python3 linit.py -o lmt1.json lmt2.json
	sed -i='' 's/"chunk-name-startswith": "<<"/"chunk-name-startswith": "@<<"/g' lmt1.json
	rm lmt1.json=
	python3 linit.py -markup markdown -o md.json
	python3 linit.py -markup -o plain.json
	python3 linit.py -markup rst -o rst.json 
	python3 linit.py -markup literate -o lrst.json
	sed -i='' 's/"to-ignore-in-chunk-startswith": "```"/"to-ignore-in-chunk-startswith": ".. code-block:: C"/g' lrst.json
	rm lrst.json=
	python3 linit.py -markup tex -o tex.json 
	-mkdir results/

sample:
	@echo "Testing LitCode on crude sample files..."
	python3 test_sample1.py > results/result_sample1.log
	python3 test_sample2.py > results/result_sample2.log
	python3 test_sample3.py > results/result_sample3.log

switch:
	@echo "Testing LitCode on a few more sample files..."
	python3 ltangle.py $(switch_files) > results/result_switch1.log
	python3 ltangle.py $(switch_files) -lmt lmt2.json > results/result_switch2.log
	python3 ltangle.py $(switch_files) -lmt lmt2.json -L -o results/Monkey_man.h
	python3 ltangle.py $(switch_files) -lmt lmt2.json -L -c 'Main.cpp' -o results/Main1.cpp
	python3 ltangle.py $(switch_files) -lmt lmt2.json -c 'case 1' -o results/case1.cpp
	python3 ltangle.py $(switch_files) -lmt lmt2.json -c 'Main.cpp' -L -t 4 -rnul -o results/Main2.cpp
	python3 ltangle.py $(switch_files) -lmt lmt2.json -c 'Main.cpp' -L -t 4 -rnul -rind 1 -o results/Main3.cpp
	python3 lweave.py $(switch_files) -lmt lmt2.json -mmt md.json -o crude/switch/doc/switch.md
	(cd crude/switch/doc/; pandoc --standalone --from=markdown --to=html switch.md -o switch.html)
	
primes: 
	@echo "Testing LitCode on primes..."
	-rm primes/primes.c primes/primes
	@echo "Tangling..."
	python3 test_primes1.py > results/result_primes.log
	python3 ltangle.py primes/primes.md -L -rnul -rind -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for markdown. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	rm primes/primes
	python3 ltangle.py primes/primes.txt -L -rnul -rind -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for plain-text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	rm primes/primes
	python3 ltangle.py primes/primes.rst -lmt lrst.json -L -rnul -rind 2 -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for restructured text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	rm primes/primes
	python3 ltangle.py primes/primes.tex -L -rnul -rind -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for LaTeX. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	@echo "Weaving..."
	python3 lweave.py primes/primes.txt -o primes/docs/primes.txt
	@echo Typesetting done for plain-text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	python3 lweave.py primes/primes.md -mmt md.json -o primes/docs/primes.md
	python3 lweave.py primes/primes.rst -lmt lrst.json -mmt rst.json -o primes/docs/primes.rst
	python3 lweave.py primes/primes.tex -mmt tex.json -o primes/docs/primes.tex
	@echo "Building typesetted docs..."
	(cd primes/docs; pandoc --standalone --from=markdown --to=html primes.md -o primes.md.html)
	@echo Typesetting done for markdown. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	(cd primes/docs; pandoc --standalone --from=rst --to=html primes.md -o primes.rst.html)
	@echo Typesetting done for restructured text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	(cd primes/docs; pdflatex primes.tex)
	@echo Typesetting done for LaTeX. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

tests-win: lmt-win sample-win switch-win primes-win

lmt-win: 
	clear
	python linit.py -o lmt1.json lmt2.json
	sed -i='' 's/"chunk-name-startswith": "<<"/"chunk-name-startswith": "@<<"/g' lmt1.json
	rm lmt1.json=
	python linit.py -markup markdown -o md.json
	python linit.py -markup -o plain.json
	python linit.py -markup rst -o rst.json 
	python linit.py -markup literate -o lrst.json
	sed -i='' 's/"to-ignore-in-chunk-startswith": "```"/"to-ignore-in-chunk-startswith": ".. code-block:: C"/g' lrst.json
	rm lrst.json=
	python linit.py -markup tex -o tex.json 
	-mkdir results/

sample-win:
	@echo "Testing LitCode on crude sample files..."
	python test_sample1.py > results/result_sample1.log
	python test_sample2.py > results/result_sample2.log
	python test_sample3.py > results/result_sample3.log

switch-win:
	@echo "Testing LitCode on a few more sample files..."
	python ltangle.py $(switch_files) > results/result_switch1.log
	python ltangle.py $(switch_files) -lmt lmt2.json > results/result_switch2.log
	python ltangle.py $(switch_files) -lmt lmt2.json -L -o results/Monkey_man.h
	python ltangle.py $(switch_files) -lmt lmt2.json -L -c 'Main.cpp' -o results/Main1.cpp
	python ltangle.py $(switch_files) -lmt lmt2.json -c 'case 1' -o results/case1.cpp
	python ltangle.py $(switch_files) -lmt lmt2.json -c 'Main.cpp' -L -t 4 -rnul -o results/Main2.cpp
	python ltangle.py $(switch_files) -lmt lmt2.json -c 'Main.cpp' -L -t 4 -rnul -rind 1 -o results/Main3.cpp
	python lweave.py $(switch_files) -lmt lmt2.json -mmt md.json -o crude/switch/doc/switch.md
	(cd crude/switch/doc/; pandoc --standalone --from=markdown --to=html switch.md -o switch.html)
	
primes-win: 
	@echo "Testing LitCode on primes..."
	-rm primes/primes.c primes/primes
	@echo "Tangling..."
	python test_primes1.py > results/result_primes.log
	python ltangle.py primes/primes.md -L -rnul -rind -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for markdown. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	rm primes/primes
	python ltangle.py primes/primes.txt -L -rnul -rind -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for plain-text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	rm primes/primes
	python ltangle.py primes/primes.rst -lmt lrst.json -L -rnul -rind 2 -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for restructured text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	rm primes/primes
	python ltangle.py primes/primes.tex -L -rnul -rind -o primes/primes.c
	(cd primes; gcc primes.c -o primes; ./primes 100)
	@echo Tangling done for LaTeX. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	@echo "Weaving..."
	python lweave.py primes/primes.txt -o primes/docs/primes.txt
	@echo Typesetting done for plain-text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	python lweave.py primes/primes.md -mmt md.json -o primes/docs/primes.md
	python lweave.py primes/primes.rst -lmt lrst.json -mmt rst.json -o primes/docs/primes.rst
	python lweave.py primes/primes.tex -mmt tex.json -o primes/docs/primes.tex
	@echo "Building typesetted docs..."
	(cd primes/docs; pandoc --standalone --from=markdown --to=html primes.md -o primes.md.html)
	@echo Typesetting done for markdown. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	(cd primes/docs; pandoc --standalone --from=rst --to=html primes.md -o primes.rst.html)
	@echo Typesetting done for restructured text. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

	(cd primes/docs; pdflatex primes.tex)
	@echo Typesetting done for LaTeX. Satisfied? [Y/n]
	@read line; if [ $$line = "n" ]; then echo aborting; exit 1 ; fi

clean:
	-rm *.json results/* primes/primes.c primes/primes
	-rm -rf __pycache__
	-rm -rf primes/docs/ results/ crude/switch/doc
	-rm litcore.py linit.py ltangle.py lweave.py