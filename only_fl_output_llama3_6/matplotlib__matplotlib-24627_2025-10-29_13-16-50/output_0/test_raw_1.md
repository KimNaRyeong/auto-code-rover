Here is the reproducer script:

```python
import matplotlib.pyplot as plt
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        f, a = plt.subplots()
        l, = a.plot([1, 2])
        l.remove()
        self.assertIsNone(l.axes)

        f, a = plt.subplots()
        l, = a.plot([1, 2])
        a.cla()
        if l.axes is not None:
            raise AssertionError("cla() should unset the .axes attribute of deparented artists")

    def run_test(self):
        try:
            self.test_issue()
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == "__main__":
    Reproducer().run_test()
```

This script creates a test case that checks the behavior of `cla()` and `remove()` methods. If the issue is present, it raises an `AssertionError` with the stack trace printed using the provided function.