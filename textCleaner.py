#! /usr/bin/python3

#
#   Clean text from src file and place in dst file   
#   
#   sentences each occupy their own line (\n splits them break).
#   three hashtags, ###, indicate a paragraph break.
#   
#
#


from sys import argv
from shutil import copyfile
from string import punctuation

if(len(argv) < 3):
    print('Please provide 1:sourcefile, 2:destinationfile')
    exit()

# if !copyfile(argv[1], argv[2]):
    # print('Failed to copy source file to destination file')
    # return False

src = open(argv[1], 'r')
dst = open(argv[2], 'w')

edge_break = '=====\n'
paragraph_break = '###\n'
sentence_break  = '\n'

checking_sentence   = False #   perform sentence checks on next characters
checking_capitol    = False #   perfor
checking_paragraph  = False #   perform paragraph checks on next characters
clearing_spaces     = False #   clear whitespace
clearing_lines      = False #   clear newlines
quote_on            = False #   quotation state toggle
abbreviation_flag   = False #   true when only one character after period
line_count          = 0     #   number of writes since last line
appellation_list    = ['Mr', 'Ms', 'Mrs', 'Dr', '..', 'A.D', 'B.C', 'N.W', 'N.E', 'S.E', 'S.W'] #   special period cases
endsentence_list    = ['.', '?', '!']   #   trigger checking_sentence flag
validstart_list     = ['-'] #   valid starting for sentences
window = []                 #   list of previous words
windowSize = 4              #   number of previous words to track

def _pushWindow(c):
    global window
    window.append(c)
    if(len(window) > windowSize):
        window.pop(0)

def _write(c):
    global quote_on
    global line_count
    global window
    global abbreviation_flag

    if quote_on and c == '"':
        quote_on = False
    elif not quote_on and c == '"':
        quote_on = True

    line_count += 1
    if c == sentence_break or c == paragraph_break:
        line_count = 0

    if c == '.':
        abbreviation_flag = 2
    elif(abbreviation_flag > 0):
        abbreviation_flag -= 1
    _pushWindow(c)
    dst.write(c)

i = 0
lookahead = 0
dst.write(edge_break)
while True:
    c = src.read(1)
    if not c:
        break

    if(clearing_lines and clearing_spaces):
        if c == ' ' or c == '\n' or c == '\r':
            continue
        else:
            clearing_lines = False
            clearing_spaces = False

    elif(clearing_spaces):
        if c == ' ':
            continue
        else:
            clearing_spaces = False

    elif(clearing_lines):
        if c == '\n' or c == '\r':
            continue
        else:
            clearing_lines = False

    if(checking_sentence):
        if c.isupper() or c in validstart_list:
            if((''.join(window[2:4]) + c) in appellation_list):
                _write(c)
                checking_sentence = False
            else:
            # checking_capitol = True
            # continue
        # elif checking_capitol and c.upper() == c:
            # _pushWindow(sentence_break)
                # dst.write(sentence_break)
                _write(sentence_break)
            # _pushWindow(c)
                # dst.write(c)
                _write(c)
                checking_sentence = False
            # clearing_spaces = True
            # line_count = 0
            continue
        elif not quote_on and c == '"':
            # _pushWindow(sentence_break)
            # _pushWindow(c)
            _write(sentence_break)
            _write(c)
            checking_sentence = False
            # line_count = 0
            continue
        elif c == '\n' or c == '\r':
            # _pushWindow(sentence_break)
            _write(sentence_break)
            checking_sentence  = False
            checking_paragraph = True
            # line_count = 0
            continue
        elif c == '"' or c == '\'':
            checking_sentence = True
            clearing_spaces = True
        else:
            checking_sentence = False
            checking_paragraph = False

    if(checking_paragraph):
        if c == ' ':
            clearing_spaces = True
            continue
        if c.isupper() and not window[-1].isupper():
            _write(sentence_break)
        if c == '\t' or c == sentence_break or c == '\r':
            if window[-1] != sentence_break:
                _write(sentence_break)
            _write(paragraph_break)
            checking_paragraph = False
            clearing_spaces = True
            clearing_lines = True
            continue
        elif line_count > 0 and window[-1] != ' ':
            _write(' ')
        checking_paragraph = False
    
    if(not abbreviation_flag and c in endsentence_list and not ''.join(window[2:4]) in appellation_list and not ''.join(window[1:4]) in appellation_list):
        checking_sentence = True
        clearing_spaces = True

    if(c == sentence_break or c == '\r'):
        checking_paragraph = True
        continue

    _write(c)
    # dst.write(c)
dst.write(edge_break)









