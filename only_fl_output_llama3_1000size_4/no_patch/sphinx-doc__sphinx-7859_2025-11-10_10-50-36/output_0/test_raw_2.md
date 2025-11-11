Here is the reproducer script:

```python
import os
import sys
from sphinx.cmd.build import main as sphinx_build
import traceback

def print_stacktrace(e: Exception):
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
        sphinx_build(['-b', 'html'])
    except ModuleNotFoundError as e:
        raise AssertionError("Issue reproduced") from e
    else:
        print("Issue not reproduced")
        sys.exit(0)

if __name__ == '__main__':
    reproduce_issue()
```

This script will run Sphinx with the `autodoc_typehints = 'descriptions'` setting and then raise an error if it fails.