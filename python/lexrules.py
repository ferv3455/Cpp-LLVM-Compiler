from functools import partial
import string
from copy import deepcopy as c

from lexer import NFA


r = NFA
n = partial(NFA, neg=True)


ALPHA = r.multipleOr(r(x) for x in string.ascii_letters)
DIGIT = r.multipleOr(r(x) for x in string.digits)

ID = (c(ALPHA) + r('_')) * (c(ALPHA) + c(DIGIT) + r('_')).star()
NUMBER = r('-').optional() * c(DIGIT).plus()
FLOAT = r('-').optional() * (c(DIGIT).plus() * r('.') * c(DIGIT).star() +
                             c(DIGIT).star() * r('.') * c(DIGIT).plus())
CHAR = r('\'') * n('\'').star() * r('\'')
STRING = r('"') * n('"').star() * r('"')

WHITESPACE = (r(' ') + r('\t') + r('\r') + r('\n')).plus()
COMMENT = r('//') * n('\n').star() * r('\n')


RULES = [
    # Preprocessor directives
    ('include', r.multipleConcat([r('#include'), r(' ').star(),
                                  r('<'), c(ID), (r('.') * c(ID)).optional(), r('>')])),
    ('define', r('#define')),

    # Keywords

    # Delimiters
    ('delimeter', r.multipleOr(r(x) for x in '([{}])')),

    # Operators
    ('bin-op', r.multipleOr(r(x) for x in '-+*/%^=&|')),
    ('unary-op', r.multipleOr([r('--'), r('++')])),
    ('rel-op', r.multipleOr([r('>'), r('>='),
                             r('=='), r('!='), r('<'), r('<=')])),
    ('logic-op', r.multipleOr([r('&&'), r('||')])),

    # Identifiers
    ('id', ID),

    # Literals
    ('int-lit', NUMBER),
    ('float-lit', FLOAT),
    ('char-lit', CHAR),
    ('str-lit', STRING),

    # Ignore whitespaces and comments
    ('comment', COMMENT, True),
    ('space', WHITESPACE, True)
]
