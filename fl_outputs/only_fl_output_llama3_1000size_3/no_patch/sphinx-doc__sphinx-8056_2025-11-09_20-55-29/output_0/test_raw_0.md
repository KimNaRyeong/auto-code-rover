Here is the reproducer script:

```python
import numpydoc as npdoc
from sphinx.ext import napoleon

def test_issue():
    try:
        docstring = """
x1, x2 : array_like, optional
    Input arrays, description of `x1`, `x2`.
"""
        npdoc.napoleon.use_numpy_doc()
        npdoc.docscan.scan(docstring)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_issue()
```

This script attempts to scan the given docstring using numpydoc's napoleon extension. If an exception is raised during scanning, it prints a stack trace and raises the same exception again.