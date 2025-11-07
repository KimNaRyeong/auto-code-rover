Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sphinx
from sphinx.ext import autodoc

def f(*, a=2**4):
    pass

def g(a=2**4):
    pass

try:
    sphinx.main()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected no error")
```

This script attempts to run Sphinx's main function, which should trigger the parsing of the argument list in the `f` and `g` functions. If the issue is present, an `AssertionError` will be raised with a stack trace that includes the line numbers of the problematic statements.