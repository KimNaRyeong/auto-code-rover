Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import unittest
from your_module import Schur_Number  # Replace 'your_module' with the actual module name

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

class TestSchurNumber(unittest.TestCase):
    def test_schur_number(self):
        # Your test case here
        self.assertEqual(Schur_Number(k), expected_result)  # Replace 'k' and 'expected_result' with actual values

if __name__ == '__main__':
    try:
        unittest.main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

Replace `'your_module'` with the actual module name where `Schur_Number` is defined, and replace `k`, `expected_result` in the test case with your actual values.