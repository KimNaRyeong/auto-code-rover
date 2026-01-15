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

def test_sympy_integer_division():
    import sympy

    s0 = sympy.Symbol('s0')
    try:
        result = sympy.Integer(1024) // s0
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e
    except Exception as e:
        # Catch any other unexpected exceptions and re-raise them as assertion errors
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.") from e
    
    print("Issue seems fixed if this message is printed.")
    return result

if __name__ == "__main__":
    test_sympy_integer_division()
