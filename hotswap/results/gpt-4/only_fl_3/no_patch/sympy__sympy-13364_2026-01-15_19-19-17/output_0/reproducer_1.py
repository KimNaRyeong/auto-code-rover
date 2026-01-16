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

def test_pow_with_mod():
    from sympy import S
    
    try:
        # Using Python's built-in pow with sympy's symbolic objects as arguments
        result = pow(S(2), S(3), S(5))
        # If we reach this point without exception, the issue is fixed
        print("No issue detected.")
        exit(0)
    except TypeError as e:
        print_stacktrace(e)
        # Failing the test if the specific exception is caught means issue exists
        assert "takes exactly 2 arguments (3 given)" in str(e), "Test failed due to an unexpected error message"

if __name__ == "__main__":
    test_pow_with_mod()
