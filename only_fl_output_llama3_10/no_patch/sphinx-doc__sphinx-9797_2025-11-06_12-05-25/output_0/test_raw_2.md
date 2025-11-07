Here is the reproducer script:

```python
import inspect
from sphinx import autodoc
from sphinx.util.docstring import prepare_docstring

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
        import sphinx
        from sphinx.ext import autodoc

        class Parent:
            @classmethod
            def method(cls) -> int:
                """Return an integer."""
                return 17

        class Child(Parent):
            @classmethod
            def method(cls):
                return 42

        doc = prepare_docstring(Child.method)
        assert "Return an integer." in doc, f"Expected method documentation to be inherited: {doc}"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script defines two classes `Parent` and `Child`, where the `method` of `Child` overrides the `method` of `Parent`. It then uses the `prepare_docstring` function to get the documentation for the overridden method. If the expected text is not found in the documentation, it raises an `AssertionError` with a stack trace.