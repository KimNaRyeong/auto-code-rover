def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_tensor_product_issue():
    from sympy import Symbol
    from sympy.physics.quantum import TensorProduct as tp
    from sympy.physics.quantum import tensor_product_simp as tps
    from sympy.physics.paulialgebra import Pauli

    a = Symbol('a', commutative=False)

    # Case 1
    t1 = tp(1,1)**2
    simplified_t1 = tps(t1)
    expected_t1 = tp(1,1)**2  # Expected to simplify but does not

    # Case 2
    t2 = tp(1, Pauli(3))**2
    simplified_t2 = tps(t2)
    expected_t2 = tp(1,1)  # Expected result from documentation/example

    try:
        assert simplified_t1 == expected_t1, "Case 1 simplification error"
        assert simplified_t2 == expected_t2, "Case 2 simplification error"
        print("All tests passed, no issue found.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_tensor_product_issue()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

sys.exit(0)
