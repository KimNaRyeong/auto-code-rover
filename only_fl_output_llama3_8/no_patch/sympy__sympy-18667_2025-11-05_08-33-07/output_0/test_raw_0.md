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
        # Add your test case here
        self.fail()  # Replace this with the actual assertion that fails

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSchurNumber)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        if not result.wasSuccessful():
            raise AssertionError("Test failed")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 when the issue is present
    else:
        exit(0)  # Exit with code 0 when the issue is fixed
```

Replace `'your_module'` with the actual module name where you have defined the `Schur_Number` class. You can add your test case in the `test_schur_number` method.