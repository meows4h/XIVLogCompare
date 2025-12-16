import math


def add_space(inp_str='', length=0):
    '''Takes an input, adds whitespace until at given length.
       Returns modified string.'''
    while len(inp_str) < length:
        inp_str += ' '
    return inp_str


def milli_to_clock(milliseconds):
    ''''''
    minutes = milliseconds / (1000 * 60)
    mins = math.floor(minutes)
    seconds = minutes - mins
    secs = math.floor(60 * seconds)
    return f'{mins}:{secs}'
