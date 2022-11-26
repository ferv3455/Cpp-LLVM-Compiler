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
    ('if', r('if')),
    ('else', r('else')),
    ('while', r('while')),
    ('for', r('for')),
    ('return', r('return')),
    ('break', r('break')),
    ('continue', r('continue')),
    ('int', r('int')),
    ('float', r('float')),
    ('char', r('char')),
    ('void', r('void')),
    ('struct', r('struct')),
    ('typedef', r('typedef')),
    ('union', r('union')),
    ('enum', r('enum')),
    ('switch', r('switch')),
    ('case', r('case')),
    ('default', r('default')),
    ('goto', r('goto')),
    ('do', r('do')),
    ('sizeof', r('sizeof')),
    ('auto', r('auto')),
    ('register', r('register')),
    ('static', r('static')),
    ('extern', r('extern')),
    ('const', r('const')),
    ('volatile', r('volatile')),
    ('signed', r('signed')),
    ('unsigned', r('unsigned')),
    ('short', r('short')),
    ('long', r('long')),
    ('double', r('double')),
    ('bool', r('bool')),
    ('true', r('true')),
    ('false', r('false')),
    ('inline', r('inline')),
    ('restrict', r('restrict')),

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
