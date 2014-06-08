markdown-toclify
================

markdown-toclify is a Python command line script that adds a **Table of Contents** with internal section-links to Markdown documents.

<br>

**Requires:**  

- [Python 2.7.x or 3.x](https://www.python.org/downloads/)
- [argparse](https://pypi.python.org/pypi/argparse)


<br>

#Usage:

The usage is quite simple, you just need to provide an Markdown-formatted input file and a file name for the output file that is to be generated.

	./markdown-toclify.py input.md output.md
	
<br>

#### Optional arguments
	
You can also add additional internal back-to-top links via the optional `-b` tag.- 

	./markdown-toclify.py input.md output.md -b
	

<br> 
Use the `-s` (`--spacer`) flag if you want to add additional vertical space (in pixels) after the table of contents.
	
	./markdown-toclify.py input.md output.md -s 100

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

## Output file

Command:

	./markdown-toclify.py input.md output.md

<br>

![Output file 1](./images/test_output_1.png)


<br>
<br>

## Output file with back-to-top links and vertical space

Command:

	./markdown-toclify.py input.md output.md -b -s 100
	
<br>

![Output file 1](./images/test_output_2.png)