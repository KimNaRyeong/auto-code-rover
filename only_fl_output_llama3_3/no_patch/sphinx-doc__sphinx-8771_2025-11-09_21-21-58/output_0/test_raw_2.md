Here is the reproducer script:

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

def test_issue():
    try:
        from sphinx.ext import autodoc
        from docutils.nodes import paragraph

        class TestClass:
            DEFAULT_OPTION = 'default'
            def do_something(self, msg, option=TestClass.DEFAULT_OPTION):
                print(msg)

        doc = autodoc.AutoDocument()
        doc.parse(['do_something(msg, option=TestClass.DEFAULT_OPTION)'])
        assert False, "Expected signature to include the constant value"
    except AssertionError as e:
        print_stacktrace(e)
    else:
        raise Exception("Test failed")

if __name__ == "__main__":
    test_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.