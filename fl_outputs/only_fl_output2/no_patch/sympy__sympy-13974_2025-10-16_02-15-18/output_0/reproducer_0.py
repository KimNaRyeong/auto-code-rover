import sys
from sympy import Symbol
from sympy.physics.quantum import TensorProduct as tp
from sympy.physics.quantum import tensor_product_simp as tps
from sympy.physics.paulialgebra import Pauli

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

def test_tensor_product_powers():
    try:
        a = Symbol('a', commutative=False)

        t1 = tp(1, 1) * tp(1, 1)
        simplified_t1 = tps(t1)
        assert simplified_t1 != t1, "Simplification of t1 did not change its expression."

        expanded_t1 = t1.expand(tensorproduct=True)
        assert expanded_t1 != t1, "Expansion of t1 did not change its expression."

        substituted_t1 = tps(tp(1, 1) * tp(1, a)).subs(a, 1)
        assert substituted_t1 == 1, "Substituted t1 is not simplified to 1."

        t2 = tp(1, Pauli(3)) * tp(1, Pauli(3))
        simplified_t2 = tps(t2)
        assert simplified_t2 != t2, "Simplification of t2 did not change its expression."

        expanded_t2 = t2.expand(tensorproduct=True)
        assert expanded_t2 != t2, "Expansion of t2 did not change its expression."

        substituted_t2 = tps(tp(1, Pauli(3)) * tp(1, a)).subs(a, Pauli(3))
        assert substituted_t2 == 1, "Substituted t2 is not simplified to 1."

        print("All tests passed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_tensor_product_powers()
    sys.exit(0)
