Here is the reproducer script:

```python
import pylint
from unittest import main, TestCase
try:
    from pyreverse import *
except ImportError:
    pass

class Reproducer(TestCase):
    def test_reproducer(self):
        name = "test_project"
        files = ["file1.py", "file2.py"]
        try:
            pylint.run_pyreverse()
        except SystemExit:
            pass  # pylint always does this.
        else:
            raise AssertionError("Expected SystemExit")

if __name__ == "__main__":
    main()
```

This script will run the `pyreverse` function and check if it raises a `SystemExit`. If not, it will raise an `AssertionError`, which should print the stack trace.