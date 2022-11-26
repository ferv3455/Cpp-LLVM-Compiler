from functools import partial
import string
from copy import deepcopy as c

from lexer import NFA as r

n = partial(r, neg=True)


ALPHA = r.alt(r(x) for x in string.ascii_letters)
DIGIT = r.alt(r(x) for x in string.digits)

ID = (c(ALPHA) + r('_')) * (c(ALPHA) + c(DIGIT) + r('_')).star()
NUMBER = r('-').optional() * c(DIGIT).plus()
FLOAT = r('-').optional() * (c(DIGIT).plus() * r('.') * c(DIGIT).star() +
                             c(DIGIT).star() * r('.') * c(DIGIT).plus())
CHAR = r('\'') * n('\'').star() * r('\'')
STRING = r('"') * n('"').star() * r('"')

WHITESPACE = r(' ') + r('\t') + r('\r') + r('\n')
COMMENT = r('//') * n('\n').star() * r('\n')


RULES = [
    # Preprocessor directives
    ('include', r.concat(r('#include'), c(WHITESPACE).star(),
                         r('<'), c(ID), (r('.') * c(ID)).optional(), r('>'))),
    ('define', r('#define')),

    # Keywords
    # TODO

    # Delimiters
    ('delimeter', r.alt(r(x) for x in '([{}])')),
    ('semicolon', r(';')),
    ('comma', r(',')),
    ('dot', r('.')),
    ('pointer', r('->')),
    ('double-colon', r('::')),

    # Operators
    ('bin-op', r.alt(r(x) for x in '-+*/%^=&|')),
    ('unary-op', r.alt(r('--'), r('++'))),
    ('rel-op', r.alt(r('>'), r('>='), r('=='), r('!='), r('<'), r('<='))),
    ('logic-op', r.alt(r('&&'), r('||'))),

    # Identifiers
    ('id', c(ID)),

    # Literals
    ('int-lit', NUMBER),
    ('float-lit', FLOAT),
    ('char-lit', CHAR),
    ('str-lit', STRING),

    # Ignore whitespaces and comments
    ('comment', COMMENT, True),
    ('space', WHITESPACE, True)
]
