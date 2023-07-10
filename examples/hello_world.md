# Hello world in C

I want to print `hello world` a 100 times in C language.

<<Hello world in C>>=
#include <stdio.h>

int main()
{
    <<Print hello world a 100 times>>
    return 0;
}
@

<<Print hello world a 100 times>>=
for (int i = 0; i < 100; ++i)
{
    fprintf(stdout, "Hello world!\n");
}
@