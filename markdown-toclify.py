#!/usr/bin/env python

#
# Sebastian Raschka 2014
#
# Python script that inserts a table of contents
# into markdown documents and creates the required
# internal links.
#
# For more information about how internal links
# in HTML and Markdown documents work, please see
#
# Creating a table of contents with internal links in 
# IPython Notebooks and Markdown documents:
# http://sebastianraschka.com/Articles/2014_ipython_internal_links.html
#
# Updates for this script will be available at 
# https://github.com/rasbt/markdown-toclify
#
#
# E.g., the structure of the table of contents
# in Markdown syntax would look like this:
#
########################################################
#
#
# - [some level1 header](#some-level1-header)
#     - [some level2 header](#some-level2-header)
#         - [some level3 header](#some-level3-header)
#   ...
# - [another level1 header](#internal link)
#
#
# <a id='some-level1-header'></a>
# # some level1 header
#
# ...
#
########################################################
#
#
# USAGE:
# 
# markdown-toclify.py input.md -o output.md
#
#

import argparse
import re

__version__ = '1.3.1'

valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'

def dashify_headline(line):
    """
    Takes a header line from a Markdown document and
    returns a tuple of the
        '#'-stripped version of the head line,
        a string version for <a id=''></a> anchor tags,
        and the level of the headline as integer.
    E.g.,
    dashify_headline('### some header lvl3')
    ('Some header lvl3', 'some-header-lvl3', 3)

    """
    stripped_right = line.rstrip('#')
    level = stripped_right.count('#')
    stripped_both = stripped_right.lstrip('#')
    stripped_wspace = stripped_both.strip()

    replaced_colon = stripped_wspace.replace('.', '')
    rem_nonvalids = ''.join([ c if c in valid_chars else ' ' for c in replaced_colon])
    dashified = '-'.join(rem_nonvalids.split(' '))
    dashified = dashified.lower()
    dashified = re.sub(r'(-)\1+', r'\1', dashified) # remove duplicate dashes
    dashified = dashified.strip('-')

    if level > 6:   # HTML supports headlines only up to <h6>
        level = 6
    return stripped_wspace, dashified, level


def get_lines(in_filename):
    """
    Returns contents of a text file as list
    of sublists that represent individual lines.

    """
    with open(in_filename, 'r') as in_file:
        in_contents = in_file.read().split('\n')
    return in_contents


def tag_and_collect(in_contents, github=False):
    """
    Creates and adds ID-anchor tags to a Markdown document content.

    Keyword arguments:
        in_contents: a list of sublists where every sublist
            represents a line from a Markdown document.
        github: If true, creates Github-compatible markdown (omits the <a id> tags)

    Returns a tuple of 2 lists:
        1st list:
            A modified version of the input list where
            <a id="some-header"></a> anchor tags where inserted
            above the header lines (if github is False).

        2nd list:
            A list of 2-value tuples, where the first value
            represents the string that was inserted assigned
            to the IDs in the anchor tags, and the second value
            is an integer that reprents the headline level.
            E.g.,
            [('some header lvl3', 'some-header-lvl3', 3), ...]

    """
    out_contents = []
    headlines = []
    for line in in_contents:
        if line.startswith(('<a id', '[[back to top](#table-of-contents)]')):
            continue
            # removes already existing modifications
        elif line.startswith('#'):
            stripped, dashed, level = dashify_headline(line)
            id_tag = '<a id="%s"></a>' %(dashed)
            headlines.append((stripped, dashed, level))
            if not github:
                out_contents.append(id_tag)

        out_contents.append(line)
    return out_contents, headlines


def create_toc(headlines, hyperlink=True):
    """
    Creates the table of contents from the headline list
    that was returned by the tag_and_collect function.

    Keyword Arguments:
        headlines: list of tuples  
            e.g., ('Some header lvl3', 'Some-header-lvl3', 3)
        hyperlink: Creates hyperlinks in Markdown format if True,
            e.g., '- [Some header lvl1](#Some-header-lvl1)'

    Returns  a list of headlines for a table of contents
    in Markdown format,
    e.g., ['        - [Some header lvl3](#Some-header-lvl3)', ...]

    """
    processed = ['#Table of Contents']
    for line in headlines:
        if hyperlink:
            item = '%s- [%s](#%s)' %((line[2]-1)*'    ', line[0], line[1])
        else:
            item = '%s- %s' %((line[2]-1)*'    ', line[0])
        processed.append(item)
    processed.append('\n')
    return processed


def add_backtotop(toc_headlines, body, github=False):
    """
    Adds internal "[back to top]" links to the Markdown document for
    jumping back to the table of contents.

    """
    if not github:
        toc_processed = ['<a id="table-of-contents"></a>\n'] + toc_headlines[:]
    else:
        toc_processed = toc_headlines[:]
    processed = []
    for line in body:
        processed.append(line)
        if line.startswith('#'):
            processed.append('[[back to top](#table-of-contents)]')
    return toc_processed, processed


def build_markdown(toc_headlines, body, spacer=0):
    """
    Returns a string with the Markdown output contents incl. 
    the table of contents.

    Keyword arguments:
        toc_headlines: lines for the table of contents
            as created by the create_toc function.
        body: contents of the Markdown file including
            ID-anchor tags as returned by the
            tag_and_collect function.
        spacer: Adds vertical space after the table
            of contents. Height in pixels.

    """
    if spacer:
        spacer_line = ['\n<div style="height:%spx;"></div>\n' %(spacer)]
        markdown = "\n".join(toc_headlines + spacer_line + body)
    else:
        markdown = "\n".join(toc_headlines + body)
    return markdown


def output_markdown(markdown_cont, outfile=None):
    """
    Prints markdown contents to the standard output screen, or
    writes to an output file if `outfile` is a valid path.

    """
    if outfile: 
        with open(outfile, 'w') as out:
            out.write(markdown_cont)
    else:
        print(markdown_cont)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Python script that inserts a table of contents\n'\
                    'into markdown documents and creates the required internal links.',
            epilog="""    Example:
    markdown-toclify.py ~/Desktop/input.md -o ~/Desktop/output.md

    For more information about how internal links in
    HTML and Markdown documents work
    please see:
    "Creating a table of contents with internal
     links in IPython Notebooks and Markdown documents"
    (http://sebastianraschka.com/Articles/2014_ipython_internal_links.html)

    Updates for this script will be available at 
    https://github.com/rasbt/markdown-toclify

    """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('InputFile', 
            metavar='input.md', 
            help='path to the Markdown input file'
            )
    parser.add_argument('-o', '--output', 
            metavar='output.md',
            default=None,
            help='path to the Markdown output file'
            )
    parser.add_argument('-b', '--back_to_top', 
            action='store_true', 
            help='add [back to top] links.'
            )
    parser.add_argument('-g', '--github', 
            action='store_true', 
            help='use Github-compatible link styles'
            )
    parser.add_argument('-s', '--spacer', 
            default=0, 
            type=int, 
            metavar='pixels',
            help='add horizontal space (in pixels) after the table of contents'
            )
    parser.add_argument('-n', '--nolink', 
            action='store_true', 
            help='create the table of contents without internal links'
            )
    parser.add_argument('-v', '--version', 
            action='version', 
            version='%s' %__version__
            )

    args = parser.parse_args()

    raw_contents = get_lines(args.InputFile)

    processed_contents, raw_headlines = tag_and_collect(raw_contents, github=args.github)
    
    processed_headlines = create_toc(raw_headlines, hyperlink=not args.nolink)

    if args.nolink:
        processed_contents = raw_contents

    if args.back_to_top:
        processed_headlines, processed_contents = add_backtotop(processed_headlines, processed_contents, github=args.github)
    
    cont = build_markdown(processed_headlines, processed_contents, args.spacer)
    output_markdown(cont, args.output)
