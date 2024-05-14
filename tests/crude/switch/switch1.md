<<Monkey_man.h>>=
fprintf(stdout, 'Monkey man!\n');

@reset
# Heading 1

@ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet mi quis tellus posuere finibus vel
vitae erat ligula.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet mi quis tellus
posuere finibus vel vitae erat ligula.  Chunks will be enclosed by `\<<` and `\>>`. Enjoy the ride, Mr. Wick.  
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet mi quis tellus posuere finibus vel
vitae erat ligula.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet mi quis tellus
posuere finibus vel vitae erat ligula.  

<<Main.cpp>>=
```Cpp
	cout \<< "Fooo\n";
	cin\>>command;
	switch(command)
	 { case 1: <<case 
	 1>>
	   case 2: <<case 2>>
	   case 3: <<case 3>>
	   case 4: <<case 4>>
	   case 5: <<case 5>>
	   case 6: <<case 6>>
	     default: <<default>>
	 }
```
@reset

# Heading 2
@ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet mi quis tellus posuere finibus
vel vitae erat ligula.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sit amet mi quis
tellus posuere finibus vel vitae erat ligula. <<case 1>> <<case 2>> <<case 3>> <<case 4>> <<case 5>> <<case 
6>> <<default>> 

<<case 1>>= 
driver dr;
dr.driver_menu();
break;

@ <<case 2>>= conductor cd;
<<case 2 conductor menu call>>
break;

@ <<case 3>>= other_employee oe;
oe.otemp_menu();
break;

@ <<case 4>>=
bus bs;
		   bs.bus_menu();
		   break;

@ Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing
elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit <<default>>.Lorem ipsum dolor sit amet, consectetur
adipiscing elit. 

<<case 5>>=
customer_menu();
break;

@ <<case 6>>=
```Cpp
clrscr();
gotoxy(32,24);
cout\<<"Exiting the program";
delay(2000);
exit(0);
break;
```

@ <<default>>=
clrscr();
gotoxy(28,24);
cout<<"\aCommand not verified";

@ Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing
elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur
adipiscing elit.

<<default>>=
```Cpp
gotoxy(28,24);
cout\<<"Try Again";
delay(2000);
break ;
```

@reset
# Heading 3
@ Full code! HHSHDOIEOIEHEOI
CONSIDER!!!  
<<Full.cpp>>=
```Cpp
	cin\>>command;
	switch(command)
	 { case 1: driver dr;
		   dr.driver_menu();
		   break;
	   case 2: conductor cd;
		   cd.conductor_menu();
		   break;
	   case 3: other_employee oe;
		   oe.otemp_menu();
		   break;
	   case 4: bus bs;
		   bs.bus_menu();
		   break;
	   case 5: customer_menu();
		   break;
	   case 6: clrscr();
		   gotoxy(32,24);
		   cout\<<"Exiting the program";
		   delay(2000);
		   exit(0);
		   break;
```