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

def test_julia_code():
    from sympy import symbols
    from sympy.printing.julia import julia_code

    x, y, A = symbols('x y A')
    code = julia_code(x**2*y*A**3)
    expected_code = "(x .^ 2 .* y) * A ^ 3"
    return code == expected_code

def main():
    try:
        assert test_julia_code(), "julia_code generates invalid Julia code"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("Test passed: julia_code output is correct.")
    exit(0)

if __name__ == "__main__":
    main()
