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

def test_imageset_with_complex_number_issue():
    from sympy import Lambda, symbols, I, S, imageset
    
    n = symbols('n')
    result = imageset(Lambda(n, 1 + I*n), S.Integers)
    
    # Check if '1' has been dropped or not
    if "1 +" not in str(result):
        raise AssertionError("The issue is present: '1' or the real part is missing from the result.")
    else:
        print("The issue appears to be fixed.")

if __name__ == "__main__":
    try:
        test_imageset_with_complex_number_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exits with error code 1 indicating an AssertionError was raised
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exits with error code 1 for any other exceptions
