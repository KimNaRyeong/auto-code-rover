import cmath
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    expression = (3 + 4*1j) / (3 - 4*1j)
    result = cmath.sqrt(expression)
    expected_result = cmath.sqrt(-1/(3 - 4*1j))*cmath.sqrt(-3 - 4*1j)
    if result != expected_result:
        raise AssertionError(f"The result is not as expected: {result} != {expected_result}")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
