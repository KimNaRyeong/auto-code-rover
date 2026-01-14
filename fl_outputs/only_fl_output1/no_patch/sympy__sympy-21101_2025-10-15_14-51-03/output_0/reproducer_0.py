# reproducer.py
def main():
    from sympy import Mul, S, latex

    # The expected output should have a space (or some form of separation) between '6' and '1/2'
    expected_output = "6 \\frac{1}{2}"
    # Compute the latex output of the unevaluated Mul
    actual_output = latex(Mul(6, S.Half, evaluate=False))

    # Raising an error if the issue is present, meaning the output is not as expected
    if actual_output.replace(" ", "") == expected_output.replace(" ", ""):  # Remove spaces to avoid false negatives
        raise AssertionError(f"Expected output to have number separation, but got '{actual_output}'")

    print("Issue not present, output:", actual_output)

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
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
