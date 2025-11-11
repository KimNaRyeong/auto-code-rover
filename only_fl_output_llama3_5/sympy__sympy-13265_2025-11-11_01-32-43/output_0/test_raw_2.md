Here is the standalone Python file `reproducer.py`:

```python
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
        m = sp.exp(sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]))
        simplified = sp.simplify(m)
        print("Simplified:")
        print(simplified)
        
        if str(simplified).find("sin(1)") == -1:
            raise AssertionError("sin(1) has not been recognized")
    except Exception as e:
        print_stacktrace(e)
        exit(-1)

if __name__ == "__main__":
    main()
```

This script will attempt to simplify the given expression using SymPy's `simplify` function. If the resulting expression does not contain "sin(1)", it will raise an `AssertionError`. The `print_stacktrace` function is used to print a stack trace of the error, including line numbers and code context.