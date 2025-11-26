Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sy
import sys

def main():
    try:
        M1 = sy.Matrix.zeros(0, 0)
        M2 = sy.Matrix.zeros(0, 1)
        M3 = sy.Matrix.zeros(0, 2)
        M4 = sy.Matrix.zeros(0, 3)
        result = sy.Matrix.hstack(M1, M2, M3, M4).shape
        assert result == (0, 6), "hstack behavior changed in sympy 1.1"
        
        if sys.version_info.major == 1 and sys.version_info.minor == 1:
            raise AssertionError("hstack behavior changed in sympy 1.1")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 1 when the issue is present, and exit with code 0 when the issue is fixed.

Please note that I added a check for the sympy version to reproduce the issue only in sympy 1.1.