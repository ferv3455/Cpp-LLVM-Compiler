from functools import partial
import string
from copy import deepcopy as c

from lexer import NFA as r

n = partial(r, neg=True)


ALPHA = r.alt(r(x) for x in string.ascii_letters)
DIGIT = r.alt(r(x) for x in string.digits)

ID = (c(ALPHA) + r('_')) * (c(ALPHA) + c(DIGIT) + r('_')).star()

CHAR_PREFIX = r('u') + r('U') + r('L') + r('u8')
CHAR = c(CHAR_PREFIX).optional() * r('\'') * n('\'').star() * r('\'')
STRING = c(CHAR_PREFIX).optional() * r('"') * n('"').star() * r('"')

NUMBER_SUFFIX = r.alt((r(x) for x in 'uUlL'), r('ll'), r('LL'))
NUMBER = r('-').optional() * c(DIGIT).plus() * c(NUMBER_SUFFIX).optional()
OCT_DIGIT = r.alt(r(x) for x in string.octdigits)
OCT_NUMBER = r('-').optional() * r('0') * \
    OCT_DIGIT.plus() * c(NUMBER_SUFFIX).optional()
HEX_DIGIT = r.alt(r(x) for x in string.hexdigits)
HEX_NUMBER = r('-').optional() * r('0x') * \
    HEX_DIGIT.plus() * c(NUMBER_SUFFIX).optional()

FLOAT_SUFFIX = r.alt(r(x) for x in 'fFlL')
FLOAT = r('-').optional() * \
    (c(DIGIT).plus() * r('.') * c(DIGIT).star() + c(DIGIT).star() * r('.') * c(DIGIT).plus()) * \
    (r('e') * r('-').optional() * c(DIGIT).plus()).optional() * \
    FLOAT_SUFFIX.optional()

MACRO = r('#') * n('\n').star() * r('\n')
COMMENT = r('//') * n('\n').star() * r('\n')
WHITESPACE = r.alt(r(x) for x in string.whitespace)


RULES = [
    # Preprocessor directives
    # ('include', r.concat(r('#include'), c(WHITESPACE).star(),
    #                      r('<'), c(ID), (r('.') * c(ID)).optional(), r('>'))),
    # ('define', r('#define')),
    ('macro', MACRO),

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

    # Punctuators
    ('parenthesis', r.alt(r(x) for x in '()')),
    ('bracket', r.alt(r(x) for x in '[]')),
    ('brace', r.alt(r(x) for x in '{}')),
    ('comma', r(',')),
    ('semicolon', r(';')),
    ('double-colon', r('::')),
    ('colon', r(':')),
    ('backslash', r('\\')),

    # Operators
    ('arithmetic-op', r.alt(r(x) for x in '+-*/%')),
    ('relational-op', r.alt(r('>'), r('>='), r('=='), r('!='), r('<'), r('<='))),
    ('logical-op', r.alt(r('&&'), r('||'), r('!'))),
    ('assignment-op', r('=')),
    ('arithm-assign-op', r.alt(r('+='), r('-='), r('*='), r('/='), r('%='))),
    ('bit-assign-op',  r.alt(r('<<='), r('>>='), r('&='), r('^='), r('|='))),
    ('increment-op', r.alt(r('--'), r('++'))),
    ('member-op', r('.')),
    ('ptr-member-op', r('->')),
    ('conditional-op', r('?')),
    ('bit-op', r.alt((r(x) for x in '~&^|'), r('<<'), r('>>'))),

    # Identifiers
    ('id', c(ID)),

    # Literals
    ('hex-lit', HEX_NUMBER),
    ('oct-lit', OCT_NUMBER),
    ('int-lit', NUMBER),
    ('float-lit', FLOAT),
    ('char-lit', CHAR),
    ('str-lit', STRING),

    # Ignore whitespaces and comments
    ('comment', COMMENT, True),
    ('space', WHITESPACE, True),

    # Catch all errors
    ('error', n()),
]
