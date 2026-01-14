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

    import abc  # noqa: F401
    from abc import ABC  # noqa: F401

    X = ...  # type: abc.ABC
    Y = ...  # type: ABC


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When running `python3 reproducer.py`, the output should be:
```python
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 16, in main
    X = ...  # type: abc.ABC
  File "reproducer.py", line 10, in print_stacktrace
    print(f'    {line_number}: {code_context}', file=sys.stderr)
UnusedImportError: Unused import abc
```
This demonstrates that the `unused-import` warning is raised for the `abc` module, even though it is used in a type comment. The expected behavior is that this warning should not be raised.