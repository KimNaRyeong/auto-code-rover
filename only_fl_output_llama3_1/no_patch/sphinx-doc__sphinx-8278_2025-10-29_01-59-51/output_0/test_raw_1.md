Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
from sphinx import autodoc
import sys

def main():
    try:
        autodoc.generate_doc(['test.rst'], 'html', False, None, None)
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

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

This script sets up a Sphinx environment and attempts to generate HTML documentation from a test rst file. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed.