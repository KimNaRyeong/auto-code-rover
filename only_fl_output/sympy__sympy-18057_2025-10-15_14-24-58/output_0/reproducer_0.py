# reproducer.py
import sympy

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

class C:
    def __repr__(self):
        return 'x.y'

def test_eq_with_repr_inducing_eval():
    try:
        _ = sympy.Symbol('x') == C()
        print("The issue with evaluating repr in __eq__ may still be present but did not trigger an exception with this example.")
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("SymPy incorrectly attempted to eval repr in its __eq__ method.") from None

def test_incorrect_equality():
    class D:
        def __repr__(self):
            return 'x'
    try:
        assert sympy.Symbol('x') != D(), "Incorrect equality comparison; repr should not influence equality."
    except AssertionError as e:
        print("Incorrect equality based on repr found.")
        raise e

if __name__ == "__main__":
    test_eq_with_repr_inducing_eval()
    test_incorrect_equality()
