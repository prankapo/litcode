---
title: Some Literate Programming Examples
author: Praneet Kapoor
email: kapoorpraneet2619@gmail.com
---

# Some Literate Programming Examples
Literate programming involves composing a symphony using a computer language. It would be best to use an
example. In this example, I will be writing a program in C to print fibonacci series. 

Being a C program, I will need to compile, link and run it. The following [Makefile](#makefile) will do all
those things. Note that it will print the first 30 terms of the fibonacci series.

<<Makefile>>=
CC := gcc -std=c99 -O0

run: fibonacci
    ./fibonacci 30

fibonacci: fibonacci.o
    $(CC) fibonacci.o -o fibonacci

fibonacci.o: fibonacci.c
    $(CC) -c fibonacci.c -o fibonacci.o
@


Now we begin writing the actual body of the cody. Fibonacci series goes as follows:
```
0 1 1 2 3 5 8 13 21 34 55... 
```

We begin by writing the [main body of the code](#fibonacci.c)
<<fibonacci.c>>=
#include <stdio.h>;
#include <stdlib.h>;
#include <string.h>;

int main(int argc, char **argv)
{
    <<Initialize variables>>
    <<Print Fibonacci series till the given number of terms>>
    return;
}
@

This is the part where we initialize some variables.

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>


<<Initialize variables>>=
int n, a, b;
a = 0;
b = 1;
<<Check whether you have been given one argument or more>>
<<Initialize n>>
@

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>

<<Check whether you have been given one argument or more>>=
if (argc < 2) {
    fprintf(stderr, "Provide 'n' as a command line argument\n");
    exit(1);
}
@

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>

<<Initialize n>>=
n = atoi(*argv[1]);
@

<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.
</p>


<<Print Fibonacci Series till the given number of terms>>=
for (int i = 0; i < n; ++i) {
    if (i < 1) {
        b = a + b;
    }
    fprintf(stdout, "%d ", a);
    a = b - a;
}
@


<<Initialize n>>=
if (n < 0) {
    fprintf(stderr, "Number of terms, n >= 0\n");
    exit(2);
}
@

