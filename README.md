markdown-toclify
================

markdown-toclify is a Python command line script that adds a **Table of Contents** with internal section-links to Markdown documents.

<br>

**Requires:**  

- [Python 2.7.x or 3.x](https://www.python.org/downloads/)
- [argparse](https://pypi.python.org/pypi/argparse)


<br>

#Usage:

The usage is quite simple, you just need to provide a Markdown-formatted input file and the modified Markdown contents will be printed to the standard output screen. 


	./markdown-toclify.py input.md
	
<br>

## Optional arguments

<br>

#### Writing to output files directly

The modified Markdown contents can be written directly to an output file instead of printing it to the standard output screen: 
	
	./markdown-toclify.py input.md -o output.md 
	
<br>
	
#### Adding "back to top" links

	
Internal "back-to-top" links can be added below each headline for jumping back to the table of contents via the optional `-b` tag. 

	./markdown-toclify.py input.md -o output.md -b
	
<br>

#### Adding vertical space after the table of contents
 
The `-s` (`--spacer`) adds additional vertical space (in pixels) after the table of contents.
	
	./markdown-toclify.py input.md -o output.md -s 100

<br>

**Examples for the in- and outputs are shown in the section below.**


<br>

#Examples

<br>
<br>

## Input file

![Input file](./images/test_input.png)

<br>
<br>

## Simple output file

Command:

	./markdown-toclify.py input.md -o output.md

<br>

![Output file 1](./images/test_output_1.png)


<br>
<br>

## Output file with back-to-top links and vertical space

Command:

	./markdown-toclify.py input.md -o output.md -b -s 100
	
<br>

![Output file 1](./images/test_output_2.png)