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
    ## number
    ('int', r('int')),
    ('float', r('float')),
    ('double', r('double')),
    ('long', r('long')),
    ('short', r('short')),
    ('unsigned', r('unsigned')),
    ('signed', r('signed')),
    ## character
    ('char', r('char')),
    ('wchar_t', r('wchar_t')),
    ('char16_t', r('char16_t')),
    ('char32_t', r('char32_t')),
    ## boolean & enum
    ('bool', r('bool')),
    ('enum', r('enum')),
    ('true', r('true')),
    ('false', r('false')),
    ## cast
    ('static_cast', r('static_cast')),
    ('dynamic_cast', r('dynamic_cast')),
    ('const_cast', r('const_cast')),
    ('reinterpret_cast', r('reinterpret_cast')),
    ## type modifier
    ('const', r('const')),
    ('volatile', r('volatile')),
    ('mutable', r('mutable')),
    ('constexpr', r('constexpr')),
    ## class and object
    ('class', r('class')),
    ('struct', r('struct')),
    ('union', r('union')),
    ('this', r('this')),
    ('new', r('new')),
    ('delete', r('delete')),
    ## class member restriction
    ('public', r('public')),
    ('protected', r('protected')),
    ('private', r('private')),
    ('override', r('override')),
    ('final', r('final')),
    ## function related
    ('void', r('void')),
    ('inline', r('inline')),
    ('explicit', r('explicit')),
    ('friend', r('friend')),
    ('virtual', r('virtual')),
    ('return', r('return')),
    ## memory designation
    ('static', r('static')),
    ('thread_local', r('thread_local')),
    ('extern', r('extern')),
    ('decltype', r('decltype')),
    ## condition statement
    ('if', r('if')),
    ('else', r('else')),
    ('switch', r('switch')),
    ('case', r('case')),
    ('default', r('default')),
    ## loop statement
    ('while', r('while')),
    ('do', r('do')),
    ('for', r('for')),
    ('break', r('break')),
    ('continue', r('continue')),
    ## type related
    ('typename', r('typename')),
    ('typeid', r('typeid')),
    ('sizeof', r('sizeof')),
    ('typedef', r('typedef')),
    ## alignment
    ('alignof', r('alignof')),
    ('alignas', r('alignas')),
    ## debug
    ('catch', r('catch')),
    ('try', r('try')),
    ('throw', r('throw')),
    ('static_assert', r('static_assert')),
    ('noexcept', r('noexcept')),
    ## other
    ('namespace', r('namespace')),
    ('using', r('using')),
    ('template', r('template')),
    ('operator', r('operator')),
    ('auto', r('auto')),
    ('export', r('export')),
    ('register', r('register')),
    ('goto', r('goto')),
    ('asm', r('asm')),
    ('volatile', r('volatile')),
    ('nullptr', r('nullptr')),

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
