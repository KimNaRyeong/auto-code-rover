Here is the reproducer script:

```python
import QQ.frac_field as F
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        x = 1.0 / 2.0
        with self.assertRaises(AssertionError) as e:
            y = not in F.QQ.frac_field(x)
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        Reproducer().test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script defines a test case that attempts to reproduce the issue. It creates an instance of `QQ.frac_field` with `x`, and then tries to use the `not in` operator on it. If the assertion error is raised, the script prints the stack trace using the provided function and exits with code 1. If no assertion error is raised, the script exits with code 0.