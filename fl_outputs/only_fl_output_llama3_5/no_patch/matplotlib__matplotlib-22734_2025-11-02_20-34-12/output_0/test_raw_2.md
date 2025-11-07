Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_tripcolor(self):
        try:
            from pylab import *
            tripcolor(np.random.rand(100), np.random.rand(100), np.random.rand(100), clim=(0, 0.5))
            colorbar()
            show()
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    Reproducer().test_tripcolor()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace.