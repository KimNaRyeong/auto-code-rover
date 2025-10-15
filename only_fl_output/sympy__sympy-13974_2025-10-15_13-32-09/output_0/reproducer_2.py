# reproducer.py
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

def main():
    from sympy import Symbol, expand
    from sympy.physics.quantum import TensorProduct as tp
    from sympy.physics.quantum import tensor_product_simp as tps
    from sympy.physics.paulialgebra import Pauli

    a = Symbol('a', commutative=False)

    # Attempt operations that should trigger an issue
    t1 = tp(1, 1) * tp(1, 1)
    t2 = tp(1, Pauli(3)) * tp(1, Pauli(3))

    try:
        # Apply simplification function
        simplified_t1 = tps(t1)
        simplified_t2 = tps(t2)

        # Check if the simplification matches the expected output
        # The issue is present if there is no change (i.e., no simplification occurred)
        assert str(simplified_t1) != "1x1**2", "t1 simplification issue present."
        assert str(simplified_t2) != "1xsigma3**2", "t2 simplification issue present."
    
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with non-zero indicating failure

    print("No issue found, simplification works as expected.")
    exit(0)

if __name__ == "__main__":
    main()
