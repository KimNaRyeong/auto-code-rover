I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
from docutils import nodes, utils

def f(*, a=2**4):
    pass

def g(a=2**4):
    pass

try:
    f()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")

try:
    g()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
```

This script defines two functions `f` and `g` with the same issue described in the bug report. It then attempts to call these functions and prints a stack trace if an exception is raised, indicating that the issue is present.