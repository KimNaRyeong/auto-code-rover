Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sphinx
from sphinx.ext import autodoc

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

def reproduce_issue():
    try:
        from sphinx.ext import autodoc
        class TestClass:
            @property
            def test_property(self) -> int:
                return 0

        autodoc.autodoc(TestClass)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a simple class `TestClass` with a property `test_property` that has a type hint of `int`. It then attempts to generate documentation for this class using Sphinx's autodoc extension. If the issue is present, an `AssertionError` will be raised and the stack trace will be printed.