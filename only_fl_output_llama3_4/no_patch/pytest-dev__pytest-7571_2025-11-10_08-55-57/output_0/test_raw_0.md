Here is the reproducer script:

```python
import pytest
from your_module import test_foo, test_bar  # replace 'your_module' with the actual name of the module that contains the failing tests

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

def main():
    try:
        pytest.main(['-v', '-s', 'reproducer.py'])
    except SystemExit as e:
        if e.code != 0:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    main()
```

This script will run the tests with the `pytest` module and catch any exceptions that are raised. If an exception is caught, it will print a stack trace using the provided function and then re-raise the exception.

Please note that you need to replace `'your_module'` with the actual name of the module that contains the failing tests.