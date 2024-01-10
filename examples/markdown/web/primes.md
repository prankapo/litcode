# Printing Prime Numbers
In this example we are going to print prime numbers. We are going to begin by first define the rules by which `primes.c` is to be built.

<<Makefile>>=
```Makefile
CC := gcc -std=c99 -O0

runprimes: primes.exe
    ./primes.exe 30

primes.exe: primes.o
    $(CC) primes.o -o primes.exe

prime.o: prime.c
    $(CC) -c primes.c -o primes.o
```

Now comes the interesting part: the C code which will print $n$ prime numbers. The core structure of our code
will be as follows:

<<primes.c>>=
```C
#include <stdio.h>
#include <stdlib.h>

int isPrime(int);

int main(int argc, char **argv)
{
    <<Initialize n>>
    <<Print prime numbers till n reaches 0>>
    return 0;
}
```


Like in the previous example, $n$ will be supplied as a command line argument.

<<Initialize n>>=
```C
int n;
if (argc < 1) {
    fprintf(stderr, "n must be supplied as a command line argument\n");
    exit(1);
}
n = atoi(argv[1]);
```

We will have a loop in which n is decremented by 1 every time a prime number is encountered. Once it reaches
0, the loop ends.

<<Print prime numbers till n reaches 0>>=
```C
int i = 0;
while (n > 0) {
    if (isPrime(i) == 0) {
        fprintf(stdout, "%d ", i);
        --n;
    }
    ++i;
}
fprintf(stdout, "Done\n");
```

In the loop, we are calling `isPrime()` to check whether the argument we have passed to it is a prime
number or not. This is done by finding the number of divisors of the argument from 2 till
$\frac{\text{argument}}{2}$. If the number of divisors is 0, then the argument is a prime number, else not.
The edge cases are for 0 and 1, which can be dealt with a simple `if` conditional statement.

<<Check if i is prime or not>>=
```C
int isPrime(int i)
{
    if (i == 0 || i == 1) {
        return 1;
    }
    for (int d = 2; d <= (i / 2); ++d) {
        if (i % d == 0) {
            return 1;
        }
    }
    return 0;
}
```

And we include it below `main()` in <<primes.c>>.

<<primes.c>>=
```C
<<Check if i is prime or not>>
```

One more thing we should do is to write rules for cleaning the directory. 

<<Makefile>>=
```Makefile
.PHONY: clean

clean: $(wildcard *.o) $(wildcard *.exe) $(wildcard *.out)
    rm -f $^
```
