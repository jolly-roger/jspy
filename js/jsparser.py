from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
import py
import sys

sys.setrecursionlimit(10000)

GFILE = py.path.local(__file__).dirpath().join('jsgrammar.txt')
try:
    t = GFILE.read(mode='U')
    regexs, rules, ToAST = parse_ebnf(t)
except Exception as e:
    print e
    raise

parsef = make_parse_function(regexs, rules, eof=True)


def parse(code):
    t = parsef(code)
    return ToAST().transform(t)
