 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import pytest

def print_stacktrace(e: Exception):
    import traceback    import sys