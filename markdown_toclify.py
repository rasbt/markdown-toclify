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
# for more information about the usage:
# markdown-toclify.py --help
#

import argparse
import re


__version__ = '1.5.1'

VALIDS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-&'


def read_lines(in_file):
    """Returns a list of lines from a input markdown file."""

    with open(in_file, 'r') as inf:
        in_contents = inf.read().split('\n')
    return in_contents


def remove_lines(lines, remove=('[[back to top]', '<a class="mk-toclify"')):
    """Removes existing [back to top] links and <a id> tags."""
    
    if not remove:
        return lines[:]
    
    out = []
    for l in lines:
        if l.startswith(remove):
            continue
        out.append(l)
    return out
    

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
    stripped_both = stripped_right.lstrip('#')
    level = len(stripped_right) - len(stripped_both)
    stripped_wspace = stripped_both.strip()

    # character replacements
    replaced_colon = stripped_wspace.replace('.', '')
    replaced_slash = replaced_colon.replace('/', '')
    rem_nonvalids = ''.join([c if c in VALIDS else '-' for c in replaced_slash])
    
    lowered = rem_nonvalids.lower()
    dashified = re.sub(r'(-)\1+', r'\1', lowered) # remove duplicate dashes
    dashified = dashified.strip('-') # strip dashes from start and end
    
    # exception '&' (double-dash in github)
    dashified = dashified.replace('-&-', '--')

    if level > 6:   # HTML supports headlines only up to <h6>
        level = 6
    return [stripped_wspace, dashified, level]
    
    
    
def tag_and_collect(lines, id_tag=True, back_links=False):
    """
    Gets headlines from the markdown document and creates anchor tags.

    Keyword arguments:
        lines: a list of sublists where every sublist
            represents a line from a Markdown document.
        id_tag: if true, creates inserts a the <a id> tags (not req. by GitHub)
        back_links: if true, adds "back to top" links below each headline

    Returns a tuple of 2 lists:
        1st list:
            A modified version of the input list where
            <a id="some-header"></a> anchor tags where inserted
            above the header lines (if github is False).

        2nd list:
            A list of 3-value sublists, where the first value
            represents the heading, the second value the string
            that was inserted assigned to the IDs in the anchor tags, 
            and the third value is an integer that reprents the headline level.
            E.g.,
            [['some header lvl3', 'some-header-lvl3', 3], ...]

    """
    out_contents = []
    headlines = []
    for l in lines:
        saw_headline = False
        if l.startswith('#'):
            saw_headline = True
            dashified = dashify_headline(l)
            if id_tag:
                id_tag = '<a class="mk-toclify" id="%s"></a>' %(dashified[1])
                out_contents.append(id_tag)
            headlines.append(dashified)
        out_contents.append(l)
        if back_links and saw_headline:
            out_contents.append('[[back to top](#table-of-contents)]')
    return out_contents, headlines
    
    
def positioning_headlines(headlines):
    """ 
    Strips unnecessary whitespaces/tabs if the first header is not left-aligned. 

    """

    left_just = False
    for row in headlines:
        if row[-1] == 1:
            left_just = True
            break
    if not left_just:
        for row in headlines:
            row[-1] -= 1
    return headlines
    

def create_toc(headlines, hyperlink=True, top_link=False):
    """
    Creates the table of contents from the headline list
    that was returned by the tag_and_collect function.

    Keyword Arguments:
        headlines: list of lists  
            e.g., ['Some header lvl3', 'some-header-lvl3', 3]
        hyperlink: Creates hyperlinks in Markdown format if True,
            e.g., '- [Some header lvl1](#some-header-lvl1)'
        top_link: if true, add a id tag for linking the table
            of contents itself (for the back-to-top-links)

    Returns  a list of headlines for a table of contents
    in Markdown format,
    e.g., ['        - [Some header lvl3](#some-header-lvl3)', ...]

    """
    
    processed = []
    if top_link:
        processed.append('<a class="mk-toclify" id="table-of-contents"></a>\n')
    processed.append('#Table of Contents')
    
    for line in headlines:
        if hyperlink:
            item = '%s- [%s](#%s)' %((line[2]-1)*'    ', line[0], line[1])
        else:
            item = '%s- %s' %((line[2]-1)*'    ', line[0])
        processed.append(item)
    processed.append('\n')
    return processed
    
    

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
            help='omits id-anchor tags (recommended for GitHub)'
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

    raw_contents = read_lines(args.InputFile)
    

    cleaned_contents = remove_lines(raw_contents, remove=('[[back to top]', '<a class="mk-toclify"'))
 
 
    processed_contents, raw_headlines = tag_and_collect(
                                            cleaned_contents, 
                                            id_tag=not args.github,
                                            back_links=args.back_to_top,
                                            )

    leftjustified_headlines = positioning_headlines(raw_headlines)

    processed_headlines = create_toc(leftjustified_headlines, hyperlink=not args.nolink,  top_link=not args.nolink and not args.github)


    if args.nolink:
        processed_contents = cleaned_contents

    cont = build_markdown(processed_headlines, processed_contents, args.spacer)
    output_markdown(cont, args.output)
