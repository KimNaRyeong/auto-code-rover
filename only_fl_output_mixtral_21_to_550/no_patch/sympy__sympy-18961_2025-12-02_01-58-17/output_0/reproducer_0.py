import sys
import sympy

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_digits_bits():
    with pytest.raises(AssertionError):
        assert sympy.ntheory.digits(-1, bits=4) == [0, 0, 0, -1]

if __name__ == "__main__":
    try:
        test_digits_bits()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(0)
