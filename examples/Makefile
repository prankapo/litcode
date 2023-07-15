#Makefile: Starts at line 5 in fibonacci.web
CC := gcc -std=C99 -O0

runfib: fibonacci.exe
	./fibonacci.exe 30

fibonacci.exe: fibonacci.o
	$(CC) fibonacci.o -o fibonacci.exe

fibonacci.o: fibonacci.c
	$(CC) -c fibonacci.c -o fibonacci.o
#Makefile: Ends at 16 in fibonacci.web
#Makefile: Extended at line 6 in primes.web
CC := gcc -std=c99 -O0

runprimes: prime.exe
	./prime.exe 30

prime.exe: prime.o
	$(CC) prime.o -o prime.exe

prime.o: prime.c
	$(CC) -c prime.c -o prime.o
#Makefile: Ends at 17 in primes.web

