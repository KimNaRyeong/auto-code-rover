Here is the reproducer script:

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
    x = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    result = sp.exp(x)
    assert not sp.simplify(result).has(sp.sin), "Simplification fails to recognize sin expressed as exponentials"
    raise AssertionError("Simplification fails to recognize sin expressed as exponentials")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.