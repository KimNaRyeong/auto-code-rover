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

def reproduce_issue():
    from sympy import symbols, imageset, Lambda, I, Integers

    n = symbols('n')
    # This is the expression that is supposed to be evaluated correctly
    image_set = imageset(Lambda(n, 1 + I*n), Integers)
    # We expect the output to include both the '1' and 'I*n', but the bug drops the '1'.
    expected_expression = "{1 + ⅈ⋅n | n ∊ ℤ}"

    # Convert both the actual and expected output to strings for comparison
    str_image_set = str(image_set)

    # Assertion to verify the bug; will not raise AssertionError if fixed
    assert str_image_set == expected_expression, "imageset result does not match expected output"

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    raise e

if __name__ == "__main__":
    import sys
    try:
        reproduce_issue()
        print("Issue seems to be fixed, exiting with code 0.")
        sys.exit(0)
    except Exception as e:
        print("An error occurred verifying the issue.")
        print_stacktrace(e)
        sys.exit(1)
