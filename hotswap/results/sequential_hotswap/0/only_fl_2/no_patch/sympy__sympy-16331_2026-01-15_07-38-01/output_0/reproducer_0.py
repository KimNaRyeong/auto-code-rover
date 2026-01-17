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

def test_ufuncify_cython_backend():
    from sympy import symbols
    from sympy.utilities.autowrap import ufuncify
    x, y = symbols('x y')
    try:
        # This will attempt to use the Cython backend for ufuncify with two arguments
        func = ufuncify((x, y), x + y, backend='Cython')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue ufuncifying a two-argument function with the Cython backend") from e

if __name__ == '__main__':
    test_ufuncify_cython_backend()
