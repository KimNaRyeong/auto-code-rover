 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback
import abc

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
    """Docstring."""

    import abc
    from abc import ABC

    X = ...  # type: abc.ABC
    Y = ...  # type: ABC
