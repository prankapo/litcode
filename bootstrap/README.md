Bootstrap Code for LitCode Development
======================================

This directory contains a prototype of litcode. It has been written like a usual piece of code and can be used
to extract and expand a particular chunk in TeX files.  
  
Setup: Giving global access
---------------------------

Run the following command in a terminal so that you can run litcode-proto from any terminal session on a
machine.

```bash
chmod +x ./bootstrap/litcode.py
sudo cp ./bootstrap/litcode.py /usr/local/bin/litcode-proto
```
  
or simply run:  

```bash
source .boostrap/build.sh
```

Using litcode-proto
-------------------
  
```bash
litcode-proto path/to/tex/files chunk/to/be/extracted single/line/comment/chars
```
  
Example 1:  

```bash
litcode-proto tests/ vector-class.cpp '//'
litcode-proto tests/ vector-header.h '//'
litcode-proto tests/ vector-play.cpp '//'
litcode-proto tests/ Makefile '#' -tabs
```
  
Example 2:  

```bash
litcode-proto tests/ litcode-tex.tex '%'
```
  
Example 3:  

```bash
litcode-proto tests/ thousand-primes.py '#'
```
  
