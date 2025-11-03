Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from unittest import TestCase

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

You can run this script by executing `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace.