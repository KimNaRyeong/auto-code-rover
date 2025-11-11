Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        try:
            mpl.rcParams['figure.autolayout'] = True
            fig, axes = plt.subplots(ncols=2)
            fig.tight_layout(w_pad=10)
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    Reproducer().test_issue()
```

This script sets the `figure.autolayout` rc parameter to `True`, then attempts to use the `tight_layout` function with a non-zero w_pad. If the issue is present, it should raise an AssertionError and print the stack trace.