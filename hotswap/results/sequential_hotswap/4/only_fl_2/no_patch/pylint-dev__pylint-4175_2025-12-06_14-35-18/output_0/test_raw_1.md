 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import subprocess
import sys
import os

def print_stacktrace(e: Exception):
    import traceback   
