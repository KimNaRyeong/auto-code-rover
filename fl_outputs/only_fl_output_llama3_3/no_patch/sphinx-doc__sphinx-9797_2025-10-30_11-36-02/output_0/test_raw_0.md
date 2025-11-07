Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from docutils.nodes import paragraph, text
from sphinx.util.docstrings import prepare_docstring

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

def test_issue():
    try:
        import spam
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

        sphinx.appbuilder.build('docs', 'build')

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected the overridden classmethod to inherit documentation from parent class")

if __name__ == "__main__":
    test_issue()
```

This script attempts to build the Sphinx documentation for the given module. If an exception is raised during this process, it prints a stack trace and raises an `AssertionError`.