//fibonacci.c: Starts at line 22 in fibonacci.web
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
//fibonacci.c: Reference at line 29 in fibonacci.web
    //Initialize variables: Starts at line 40 in fibonacci.web
    int a, b, n;
    a = -1;
    b = 1;
    //Initialize variables: Reference at line 44 in fibonacci.web
    //Check cmd args and Initialize n: Starts at line 47 in fibonacci.web
    if (argc < 2) {
        fprintf(stderr, "Please provide `n' as a command line argument\n");
        exit(1);
    }
    else {
        n = atoi(argv[1]);
    }
    //Check cmd args and Initialize n: Ends at 55 in fibonacci.web
    //Check cmd args and Initialize n: Extended at line 60 in fibonacci.web
    if (n < 0) {
        fprintf(stderr, "n >= 0\n");
        exit(1);
    }
    //Check cmd args and Initialize n: Ends at 65 in fibonacci.web
    //Initialize variables: Continues from line 45 in fibonacci.web
    //Initialize variables: Ends at 45 in fibonacci.web
//fibonacci.c: Continues from line 30 in fibonacci.web
//fibonacci.c: Reference at line 30 in fibonacci.web
    //Generate Fibonacci series till n terms: Starts at line 69 in fibonacci.web
    for (int i = 0; i < n; ++i) {
        fprintf(stdout, "%d ", a + b);
        b = b + a;
        a = b - a;
    }
    //Generate Fibonacci series till n terms: Ends at 75 in fibonacci.web
//fibonacci.c: Continues from line 31 in fibonacci.web
    fprintf(stdout, "Done\n");
    return 0;
}
//fibonacci.c: Ends at 34 in fibonacci.web

