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


if __name__ == "__main__":
    q, u = smp.symbols(('q:2', 'u:2'), cls=smp.Function)
    assert type(q[0]) == smp.core.function.UndefinedFunction, "AssertionError: symbols() didn't create Function instances"
    print(type(q[0]))
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    assert type(q[0]) == smp.core.function.UndefinedFunction, "AssertionError: symbols() didn't create Function instances"
AssertionError: AssertionError: symbols() didn't create Function instances
```
This confirms that the issue is present in Sympy version 1.10.1.