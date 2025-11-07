Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication
from sphinx.util import logging
import requests
import sys
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

def reproducer():
    try:
        sphinx_app = SphinxApplication()
        sphinx_app.config.linkcheck_workers = True
        sphinx_app.build_file('source/index.rst', 'build')
        if not os.path.exists('build/anchor-not-found.txt'):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproducer()
```

This script attempts to build a Sphinx project with link checking enabled. If the expected file is not created, it raises an AssertionError indicating that the issue was not reproduced.

To run the reproducer, save the above code in a file named `reproducer.py`, navigate to the root directory of your project, and execute the script using `python3 reproducer.py`.