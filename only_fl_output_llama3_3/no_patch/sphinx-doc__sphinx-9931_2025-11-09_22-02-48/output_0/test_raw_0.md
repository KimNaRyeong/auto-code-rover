Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from sphinx.util import logging

def main():
    try:
        conf = sphinx.config.Config()
        conf.add_module_names = False
        autodoc.process_nodoc(conf, ['mypackage/mymodule.py'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()

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
```

This script attempts to reproduce the issue by setting `add_module_names` to `False` and then processing a Python module using Sphinx's autodoc. If the issue is present, it prints the stack trace and raises an assertion error.