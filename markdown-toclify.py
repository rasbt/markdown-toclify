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
# USAGE:
#
# markdown-toclify.py input.md output.md
#
#
#

import argparse

__version__ = '1.0.1'

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
    stripped_pound = line.strip('#')
    level = len(line) - len(stripped_pound)
    stripped_space = stripped_pound.strip()
    dashified = "-".join(stripped_space.split(' '))
    return stripped_space, dashified, level


def get_lines(in_filename):
    """
    Returns contents of a text file as list
    of sublists that represent individual lines.

    """
    with open(in_filename, 'r') as in_file:
        in_contents = in_file.read().split('\n')
    return in_contents


def tag_and_collect(in_contents):
    """
    Creates and adds ID-anchor tags to a Markdown document content.

    Keyword arguments:
        in_contents: a list of sublists where every sublist
            represents a line from a Markdown document.

    Returns a tuple of 2 lists:
        1st list:
            A modified version of the input list where
            <a id="some-header"></a> anchor tags where inserted
            above the header lines.

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
            out_contents.append(id_tag)

        out_contents.append(line)

    return out_contents, headlines


def create_toc(headlines):
    """
    Takes a list of tuples,
    e.g., ('Some header lvl3', 'Some-header-lvl3', 3)
    and returns a list of headlines for a table of contents
    in Markdown format,
    e.g., ['        - [Some header lvl3](#Some-header-lvl3)', ...]

    """
    processed = ['#Table of Contents']
    for line in headlines:
        item = '%s- [%s](#%s)' %((line[2]-1)*'    ', line[0], line[1])
        processed.append(item)
    return processed


def add_backtotop(toc_headlines, body):
    """
    Adds internal "[back to top]" links to the Markdown document for
    jumping back to the table of contents.

    """
    toc_processed = ['<a id="table-of-contents"></a>\n'] + toc_headlines[:]
    processed = []
    for line in body:
        processed.append(line)
        if line.startswith('#'):
            processed.append('[[back to top](#table-of-contents)]')
    return toc_processed, processed


def write_markdown(out_file, toc_headlines, body, spacer=0):
    """
    Writes the Markdown output file with the table of
    contents.

    Keyword arguments:
        out_file: Path to the output file.
        toc_headlines: lines for the table of contents
            as created by the create_toc function.
        body: contents of the Markdown file including
            ID-anchor tags as returned by the
            tag_and_collect function.
        spacer: Adds vertical space after the table
            of contents. Height in pixels.

    """
    with open(out_file, 'w') as out:
        for line in toc_headlines:
            out.write(line + '\n')
        if spacer:
            out.write('\n<div style="height:%spx;"></div>\n' %(spacer))
        out.write(4 * '\n')
        for line in body:
            out.write(line + '\n')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Python script that inserts a table of contents\n'\
                    'into markdown documents and creates the required internal links.',
            epilog="""    Example:
    markdown-toclify.py ~/Desktop/input.md  ~/Desktop/output.md

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
            metavar=('input.md'), 
            help='Path to the Markdown input file.'
            )
    parser.add_argument('OutputFile', 
            metavar=('output.md'),
            help='Path to the Markdown output file.'
            )
    parser.add_argument('-b', '--back_to_top', 
            action='store_true', 
            help='Adds [back to top] links.'
            )
    parser.add_argument('-s', '--spacer', 
            default=0, 
            type=int, 
            metavar=('pixels'),
            help='Adds horizontal space (in pixels) after the table of contents'
            )
    parser.add_argument('-v', '--version', 
            action='version', 
            version='%s' %__version__
            )

    args = parser.parse_args()

    raw_contents = get_lines(args.InputFile)
    tagged_contents, raw_headlines = tag_and_collect(raw_contents)
    processed_headlines = create_toc(raw_headlines)

    if args.back_to_top:
        processed_headlines, tagged_contents = add_backtotop(processed_headlines, tagged_contents)

    write_markdown(args.OutputFile, processed_headlines, tagged_contents, args.spacer)
