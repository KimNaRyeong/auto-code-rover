from sympy import *
from sympy.physics.quantum import TensorProduct as tp
from sympy.physics.quantum import tensor_product_simp as tps
from sympy.physics.paulialgebra import Pauli
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

a = Symbol('a', commutative=False)
t1 = tp(1,1)*tp(1,1)
assert tps(t1) == 1, "Issue: tensor_product_simp failed to simplify t1"
assert t1.expand(tensorproduct=True) == 1, "Issue: expand(tensorproduct=True) failed to expand t1"
t2 = tp(1,Pauli(3))*tp(1,Pauli(3))
assert tps(t2) == 1, "Issue: tensor_product_simp failed to simplify t2"
assert t2.expand(tensorproduct=True) == 1, "Issue: expand(tensorproduct=True) failed to expand t2"
t3 = tp(1,Pauli(3))*tp(1,a)
t3_subs = t3.subs(a, Pauli(3))
assert tps(t3_subs) == tp(1,1), "Issue: tensor_product_simp failed to simplify t3_subs"
