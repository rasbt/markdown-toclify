# The test.py script can be run by either py.test or nosetests
# from the main markdown-toclify directory
#
# e.g.,
# bash> nosetests
# bash> py.test tests.py

import markdown_toclify as mt



def test_remove_lines():
    in1 = ['This is a test', '#abc', 
           '<a class="mk-toclify" id="test">hello</a>',
           'line',
           '[[back to top](#table-of-contents)] hello',
           'last line',
           ]
    out1 = ['This is a test', '#abc', 
           'line',
           'last line',
           ]
           
    assert(mt.remove_lines(in1) == out1)
    
    
    
def test_dashify_headline():
    in1 = '### some headline lvl3'
    in2 = '########some headline lvl7'
    in3 = '########So/me head--line lvl7######'
    
    assert(mt.dashify_headline(in1) == ['some headline lvl3', 'some-headline-lvl3', 3])
    assert(mt.dashify_headline(in2) == ['some headline lvl7', 'some-headline-lvl7', 6])
    assert(mt.dashify_headline(in3) == ['So/me head--line lvl7', 'some-head-line-lvl7', 6])
    

def test_tag_and_collect():
    in1 = ['# first headline', 
           'some text',
           '## second headline',
           'more text'
           ]
           
    out1_1 = ['<a id="first-headline"></a>', 
           '# first headline', 
           'some text', 
           '<a id="second-headline"></a>', 
           '## second headline', 
           'more text'
           ] 
    out1_2 = [
             ['first headline', 'first-headline', 1], 
             ['second headline', 'second-headline', 2]
             ]
             
    out2_1 = ['# first headline', 
           'some text', 
           '## second headline', 
           'more text'
           ] 
    out2_2 = [
             ['first headline', 'first-headline', 1], 
             ['second headline', 'second-headline', 2]
             ]

    assert(mt.tag_and_collect(in1, id_tag=True) == out1_1, out1_2)
    assert(mt.tag_and_collect(in1, id_tag=False) == out2_1, out2_2)
    

def test_positioning_headlines():
    in1 = [['first headline', 'first-headline', 1], 
           ['second headline', 'second-headline', 2]]
    in2 = [['first headline', 'first-headline', 2], 
           ['second headline', 'second-headline', 3]]      
           
    assert(mt.positioning_headlines(in1) == in1)
    assert(mt.positioning_headlines(in2) == in1)
    

def test_create_toc():
    in1 = [['first headline', 'first-headline', 1], 
           ['second headline', 'second-headline', 2]]
           
    out1 = ['#Table of Contents', 
            '- [first headline](#first-headline)',
            '    - [second headline](#second-headline)', '\n'
           ]
    out2 = ['<a class="mk-toclify" id="table-of-contents"></a>\n',
            '#Table of Contents', 
            '- [first headline](#first-headline)',
            '    - [second headline](#second-headline)', '\n'
           ]
           
    assert(mt.create_toc(in1, hyperlink=True, top_link=False) == out1)
    assert(mt.create_toc(in1, hyperlink=True, top_link=True) == out2)
    


        


