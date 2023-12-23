//primes.c: Starts at line 100 in web/examples.web
#include <stdio.h>
#include <stdlib.h>

int isPrime(int);

int main(int argc, char **argv)
{
//primes.c: Reference at line 108 in web/examples.web
    //Initialize n: Starts at line 117 in web/examples.web
    int n;
    if (argc < 1) {
        fprintf(stderr, "n must be supplied as a command line argument\n");
        exit(1);
    }
    n = atoi(argv[1]);
    //Initialize n: Ends at 124 in web/examples.web
//primes.c: Continues from line 109 in web/examples.web
//primes.c: Reference at line 109 in web/examples.web
    //Print prime numbers till n reaches 0: Starts at line 129 in web/examples.web
    int i = 0;
    while (n > 0) {
        if (isPrime(i) == 0) {
            fprintf(stdout, "%d ", i);
            --n;
        }
        ++i;
    }
    fprintf(stdout, "Done\n");
    //Print prime numbers till n reaches 0: Ends at 139 in web/examples.web
//primes.c: Continues from line 110 in web/examples.web
    return 0;
}
//primes.c: Ends at 112 in web/examples.web
//primes.c: Extended at line 163 in web/examples.web
//primes.c: Reference at line 164 in web/examples.web
//Check if i is prime or not: Starts at line 146 in web/examples.web
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
//Check if i is prime or not: Ends at 159 in web/examples.web
//primes.c: Continues from line 165 in web/examples.web
//primes.c: Ends at 165 in web/examples.web

