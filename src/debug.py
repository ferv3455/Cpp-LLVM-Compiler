from functools import partial
import string
from copy import deepcopy as c

from mycompiler.lexer import NFA as r

n = partial(r, neg=True)


# Define the automata and input here
DIGIT = r.alt(r(x) for x in string.digits)
FLOAT_SUFFIX = r.alt(r(x) for x in 'fFlL')
FLOAT = r('-').optional() * \
    (c(DIGIT).plus() * r('.') * c(DIGIT).star() + c(DIGIT).star() * r('.') * c(DIGIT).plus()) * \
    (r('e') * r('-').optional() * c(DIGIT).plus()).optional() * \
    FLOAT_SUFFIX.optional()
text = '-.4e2 '

# Run
i = FLOAT.simulate(text)
print("match length:", i)
print(text[:i])
