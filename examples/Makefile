#Makefile: Starts at line 6 in web/examples.web
CC := gcc -std=C99 -O0

runfib: fibonacci.exe
	./fibonacci.exe 30

fibonacci.exe: fibonacci.o
	$(CC) fibonacci.o -o fibonacci.exe

fibonacci.o: fibonacci.c
	$(CC) -c fibonacci.c -o fibonacci.o
#Makefile: Ends at 17 in web/examples.web
#Makefile: Extended at line 84 in web/examples.web
CC := gcc -std=c99 -O0

runprimes: primes.exe
	./primes.exe 30

primes.exe: primes.o
	$(CC) primes.o -o primes.exe

prime.o: prime.c
	$(CC) -c primes.c -o primes.o
#Makefile: Ends at 95 in web/examples.web
#Makefile: Extended at line 169 in web/examples.web

.PHONY: clean

clean: $(wildcard *.o) $(wildcard *.exe) $(wildcard *.out)
	rm -f $^
#Makefile: Ends at 175 in web/examples.web

