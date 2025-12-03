from sympy import *
from sympy.physics.quantum import TensorProduct as tp
from sympy.physics.quantum import tensor_product_simp as tps
from sympy.physics.paulialgebra import Pauli
import traceback    # import traceback and sys here, instead of inside the function
import sys

def print_stacktrace(e: Exception):
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
t2 = tp(1,Pauli(3))*tp(1,Pauli(3))

tps(t1)
t1.expand(tensorproduct=True)

tps(tp(1,Pauli(3))*tp(1,a)).subs(a, Pauli(3))

expected_result_t1 = 1
assert tps(t1) == expected_result_t1, f"tps(t1) should be equal to {expected_result_t1}"
print("tps(t1) is equal to the expected result")

expected_result_t2 = tp(1,Pauli(3))**2
assert tps(tp(1,Pauli(3))*tp(1,a)).subs(a, Pauli(3)) == expected_result_t2, f"tps(tp(1,Pauli(3))*tp(1,a)).subs(a, Pauli(3)) should be equal to {expected_result_t2}"
print("tps(tp(1,Pauli(3))*tp(1,a)).subs(a, Pauli(3)) is equal to the expected result")
