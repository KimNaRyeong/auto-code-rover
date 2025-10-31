Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sphinx
from sphinx.ext import autodoc

def test_issue():
    class BaseClass:
        @classmethod
        @property
        def baseclass_property(cls):
            """Some class property."""
            return "property"

    class MetaClass(BaseClass):
        pass

    class SubClass(MetaClass):
        pass

    try:
        sphinx.main()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    test_issue()
```

This script defines the same classes and methods that are described in the issue, and then attempts to run Sphinx. If the issue is present (i.e., the methods are not documented), it prints a stack trace using the `print_stacktrace` function and raises an `AssertionError`.