Here is the standalone Python file `reproducer.py` to reproduce the issue:

```py
import sympy as sp

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

def main():
    try:
        poly = sp.Poly(1.2*sp.Symbol('x')*sp.Symbol('y')*sp.Symbol('z'), sp.Symbol('x'), domain='RR[y,z]')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected Poly to be created without raising an error")

if __name__ == "__main__":
    main()
```

This script should reproduce the issue and print a stack trace when executed with `python3 reproducer.py`.