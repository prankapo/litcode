//fibonacci.c: Starts at line 23 in web/examples.web
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
//fibonacci.c: Reference at line 30 in web/examples.web
    //Initialize variables: Starts at line 41 in web/examples.web
    int a, b, n;
    a = -1;
    b = 1;
    //Initialize variables: Reference at line 45 in web/examples.web
    //Check cmd args and Initialize n: Starts at line 48 in web/examples.web
    if (argc < 2) {
        fprintf(stderr, "Please provide `n' as a command line argument\n");
        exit(1);
    }
    else {
        n = atoi(argv[1]);
    }
    //Check cmd args and Initialize n: Ends at 56 in web/examples.web
    //Check cmd args and Initialize n: Extended at line 61 in web/examples.web
    if (n < 0) {
        fprintf(stderr, "n >= 0\n");
        exit(1);
    }
    //Check cmd args and Initialize n: Ends at 66 in web/examples.web
    //Initialize variables: Continues from line 46 in web/examples.web
    //Initialize variables: Ends at 46 in web/examples.web
//fibonacci.c: Continues from line 31 in web/examples.web
//fibonacci.c: Reference at line 31 in web/examples.web
    //Generate Fibonacci series till n terms: Starts at line 70 in web/examples.web
    for (int i = 0; i < n; ++i) {
        fprintf(stdout, "%d ", a + b);
        b = b + a;
        a = b - a;
    }
    //Generate Fibonacci series till n terms: Ends at 76 in web/examples.web
//fibonacci.c: Continues from line 32 in web/examples.web
    fprintf(stdout, "Done\n");
    return 0;
}
//fibonacci.c: Ends at 35 in web/examples.web

