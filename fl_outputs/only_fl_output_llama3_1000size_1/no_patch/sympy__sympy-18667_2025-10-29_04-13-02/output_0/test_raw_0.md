Here is the `reproducer.py` script that reproduces the issue:

```python
import unittest
from your_module import combinatorics  # Replace 'your_module' with the actual module name

class TestSchurNumber(unittest.TestCase):
    def test_schur_number(self):
        self.assertEqual(combinatorics.Schur_Number(1), 2)  # Add your expected result here

if __name__ == '__main__':
    try:
        unittest.main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

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

```

Please replace `'your_module'` with the actual name of your module where `combinatorics.Schur_Number(1)` is defined.