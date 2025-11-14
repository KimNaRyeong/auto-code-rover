print("Reproducing issue...")

import sympy as sp
from sympy import *

n = sp.symbols('n')
result = bell(n).limit(n, sp.oo)

print(f"Result: {result}")

if result != sp.oo:
    try:
        assert False, "bell(n).limit(n, oo) should be oo"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

print("Issue not present!")
exit(0)
