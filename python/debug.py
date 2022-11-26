from functools import partial
import string
from copy import deepcopy as c

from lexer import NFA as r

n = partial(r, neg=True)


# Define the automata and input here
# COMMENT = r('//') * n('\n').star() * r('\n')
COMMENT = n().star() * r('y')
text = '// uiygi\n'

# Run
i = COMMENT.simulate(text)
print("match length:", i)
print(text[:i])
