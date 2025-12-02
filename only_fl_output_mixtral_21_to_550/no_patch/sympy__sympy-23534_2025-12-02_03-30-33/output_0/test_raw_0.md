 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy as smp


def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def main():
    q, u = smp.symbols(('q:2', 'u:2'), cls=smp.Function)
    assert type(q[0]) == smp.core.function.UndefinedFunction, "Symbols were created instead of Functions"


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present. The script exits with a non-zero exit code. When the issue is fixed, the script will exit with a zero exit code.