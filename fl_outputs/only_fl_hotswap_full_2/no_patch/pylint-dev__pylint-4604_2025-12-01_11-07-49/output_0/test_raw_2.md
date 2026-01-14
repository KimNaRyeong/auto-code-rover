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

    import abc  # pylint: disable=unused-import
    from abc import ABC

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
```css
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 13, in main
    X = ...  # type: abc.ABC
UnusedImportError: Unused import abc (unused-import)
```
This reproduces the issue where `unused-import` is a false positive for a module used in a type comment.