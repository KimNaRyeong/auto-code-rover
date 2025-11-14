Here is a sample `reproducer.py` file that you can use as a starting point:

```python
import unittest
from your_module import YourClass  # replace with the actual module and class name

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

class TestReproducer(unittest.TestCase):
    def test_reproduce_issue(self):
        try:
            # Your code to reproduce the issue goes here
            your_object = YourClass()
            your_object.your_method()  # replace with the actual method name
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    unittest.main(exit=False)

```

This script uses the `unittest` module to run a single test case. The test case attempts to reproduce the issue by calling your code. If an `AssertionError` is raised, it prints the stack trace using the `print_stacktrace` function and then re-raises the exception.

To use this script, replace `your_module`, `YourClass`, and `your_method` with the actual names of the module, class, and method that you want to test. Then, run the script using `python3 reproducer.py`. If the issue is present, it will print a stack trace showing the line numbers of the statements.