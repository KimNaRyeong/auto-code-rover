Here is the reproducer script:

```python
import unittest
from your_module import interpolate  # replace 'your_module' with the actual module name where interpolate function is defined

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

class TestInterpolate(unittest.TestCase):

    def test_interpolate(self):
        y = (18, 25, 43, 70, 115)
        try:
            result = interpolate(y, 5)
            self.assertFalse(np.isnan(result) or result == 115)
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == '__main__':
    unittest.main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.