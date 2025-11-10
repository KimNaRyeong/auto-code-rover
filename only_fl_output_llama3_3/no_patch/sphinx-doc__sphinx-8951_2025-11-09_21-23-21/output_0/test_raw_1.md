Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sphinx
from docutils import nodes, util
from sphinx.util.nodes import process_directive

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

try:
    process_directive('cpp:function', 'std::strong_ordering operator<=>(Foo, Foo)')
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error"
```

This script attempts to process a C++ function declaration using Sphinx's `process_directive` function. If the processing fails due to the spaceship operator issue, it prints the stack trace and raises an `AssertionError`.