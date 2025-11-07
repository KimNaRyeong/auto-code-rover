Here is the reproducer script:

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
    raise AssertionError("Issue not fixed")
```

This script should be run with `python3 reproducer.py` and it will attempt to reproduce the issue. If the issue is present, it will print a stack trace and raise an `AssertionError`.