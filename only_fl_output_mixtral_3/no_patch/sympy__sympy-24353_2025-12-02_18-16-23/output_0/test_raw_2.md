 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys

def print_stacktrace(e: Exception):
    import traceback   
