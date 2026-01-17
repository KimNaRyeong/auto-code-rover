# reproducer.py
def main():
    from sympy import Symbol, MatrixSymbol, Add, MatAdd

    try:
        # Reproduce issue with Add vs MatAdd behavior
        x = Symbol('x')
        A = MatrixSymbol('A', 2, 2)

        # Test Add evaluation
        add_result = Add(x, x, evaluate=True)
        assert add_result != Add(x, x, evaluate=False), "Add evaluates incorrectly when evaluate=True vs evaluate=False"

        # Test MatAdd without evaluate keyword, expecting similar behavior as Add
        matadd_result = MatAdd(A, A)  # Default should behave as if evaluate=True if implemented
        assert matadd_result != MatAdd(A, A, evaluate=False), "MatAdd doesn't support evaluate argument or behaves incorrectly"

        # Check if specifying evaluate=True explicitly changes the behavior
        evaluated_matadd_result = MatAdd(A, A, evaluate=True)
        assert evaluated_matadd_result == 2 * A, "MatAdd with evaluate=True does not canonicallize to 2*A"

    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    main()
