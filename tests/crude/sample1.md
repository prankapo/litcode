@ Foo bar is barred from fooing in the bar
foo bar is not innocent <<When 1, take a piss>>, I feel relaxed!
<<So take a good piss>>Romeo! As can be seen, the initial few characters on this line were considered as a
chunk reference. 
@reset 

@This line won't be considered as a new module.
@ But this line will be considered as one! @red

@<<isprime()>>=
```C
Gulmira ka sipahi
<<Program header>>
int isprime(uint64_t n) {
	uint64_t d, d_count;
	for (d = 1, d_count = 1; d <= n / 2; ++d) {
		if (n % d == 0) {
			++d_count;
		}
		if (d_count > 1) {
			break;
		}
	}
	--d_count;	/* Step 6 */
	switch (d) {
		case 1: <<When 1, take a piss>>
		case 2: <<When 2, you need to go to argentina where you will encounter a commodo dragon. Befriend that dragon and return home 
		to your mistress>>
	}
	return 0;
}
```

@reset
@ In this module we wish to check whether the lexer characterizes the @ sign as a new-module-startswith
character or not. It should not!
In the 24th century, men were lizard, women were snakes, and kids don't exist!! Everyome works 45 hrs a week @
9 hrs / day!

@ @<<another_func()>>+=
```C
for (int i = 100; i >= 0; --i) {
	fprintf(stdout, 'Michael Jackson is dead!\n');
}
```

@ In this module we wish to check whether the lexer characterizes the @<<Dummy Value>>= as a chunk definition
or not. It should not!!

@ The following is a valid chunk definition, copied from https://www.geeksforgeeks.org/decorators-in-python/:

@<<Python decorators!>>=
```Python
# importing libraries
import time
import math

# decorator to calculate duration
# taken by any function.
def calculate_time(func):
	# added arguments inside the inner1,
	# if function takes any arguments,
	# can be added like this.
	def inner1(*args, **kwargs):
		# storing time before function execution
		begin = time.time()
		func(*args, **kwargs)
		# storing time after function execution
		end = time.time()
		print("Total time taken in : ", func.__name__, end - begin)
	return inner1

# this can be added to any function present,
# in this case to calculate a factorial
@calculate_time
def factorial(num):
	# sleep 2 seconds because it takes very less time
	# so that you can see the actual difference
	print('You get decorators by using @ sign!')
	time.sleep(2)
	print(math.factorial(num))

# calling the function.
factorial(10)
```

@ How will we deal with the following??
Random text1: sin(x) \<< 1 for x -> 0.  
Random text2: tan(x) \>> 0 for x -> 90.  
Random text3: The symbol `@<<` starts the chunk definition header and the symbol `>>=` ends it, whereas `\<<`
starts a chunk reference and `\>>` ends it. 

@ A kicker:
@<<Crickey!>>+=
```C++
#include <iostream>

int main(int argc, char ** argv) {
	std::cout \<< "Hello, world!" \<< std::endl;
	char ch;
	std::cin \>> ch;
	int p1;
	std::cout \<< "Person 1:", std::cin \>> p1;
	int p1 = (std::cin \>> (std::cout \<< "Person 1: ", p1), p1);
	return 0;
}
```
