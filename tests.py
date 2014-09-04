# The test.py script can be run by either py.test or nosetests
# from the main markdown-toclify directory
#
# e.g.,
# bash> nosetests
# bash> py.test tests.py

import markdown_toclify as mt


def test_markdown_std(): 
    # new markdown standards (makdown-toclify > 1.6)
    # see http://jgm.github.io/stmd/spec.html#atx-headers
       
    ex23 = ['# foo',
            '## foo',
            '### foo',
            '#### foo',
            '##### foo',
            '###### foo']   
    out23 = [['foo', 'foo', 1], ['foo', 'foo', 2], ['foo', 'foo', 3], 
            ['foo', 'foo', 4], ['foo', 'foo', 5], ['foo', 'foo', 6]]        
    assert(mt.tag_and_collect(ex23, id_tag=False)[1] == out23)        
    
    # More than six # characters is not a header:
    ex24 = ['# first headline', 
           'some text',
           '####### no headline',
           'more text'
           ]
    out24 = [['first headline', 'first-headline', 1]]
    assert(mt.tag_and_collect(ex24, id_tag=False)[1] == out24)        
       
    # A space is required between the # characters and the header’s content:
    ex25 = ['# first headline',  
           'some text',
           '##no headline',
           'more text'
           ]
    out25 = [['first headline', 'first-headline', 1]]
    assert(mt.tag_and_collect(ex25, id_tag=False)[1] == out25)
    
    # This is not a header, because the first # is escaped:
    ex26 = ['# first headline',  
           'some text',
           '\## no headline',
           'more text'
           ]
    out26 = [['first headline', 'first-headline', 1]]
    assert(mt.tag_and_collect(ex26, id_tag=False)[1] == out26)
    
    # Leading and trailing blanks are ignored in parsing inline content:
    ex28 = ['#           first headline',  
           'some text',
           'more text'
           ]
    out28 = [['first headline', 'first-headline', 1]]
    assert(mt.tag_and_collect(ex28, id_tag=False)[1] == out28)
    

    # One to three spaces indentation are allowed:
    ex29 = ['   # first headline', 
           'some text',
           '    ## no headline',
           'more text'
           ]
    out29 = [['first headline', 'first-headline', 1]]
    assert(mt.tag_and_collect(ex29, id_tag=False)[1] == out29)

    # A closing sequence of # characters is optional:
    ex32 = ['## first headline ##', 
           'some text',
           'more text'
           ]
    out32 = [['first headline', 'first-headline', 2]]
    assert(mt.tag_and_collect(ex32, id_tag=False)[1] == out32)

    # It need not be the same length as the opening sequence:
    ex33 = ['## first headline ####', 
           'some text',
           'more text'
           ]
    out33 = [['first headline', 'first-headline', 2]]
    assert(mt.tag_and_collect(ex33, id_tag=False)[1] == out33)

    #A sequence of # characters with a nonspace character following it 
    # is not a closing sequence, but counts as part of the contents of the header:
    ex34 = ['## first  #### headline', 
           'some text',
           'more text'
           ]
    print(mt.tag_and_collect(ex34, id_tag=False)[1])
    out34 = [['first  #### headline', 'first-headline', 2]]
    assert(mt.tag_and_collect(ex34, id_tag=False)[1] == out34)


    ## ignore empty header
    ex35 = ['# first headline', 
           '## ######',
           'more text'
           ]
    print(mt.tag_and_collect(ex35, id_tag=False)[1])
    out35 = [['first headline', 'first-headline', 1]]
    assert(mt.tag_and_collect(ex35, id_tag=False)[1] == out35)



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
    
    assert(mt.dashify_headline(in1) == ['some headline lvl3', 'some-headline-lvl3', 3])

    

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
    


        


