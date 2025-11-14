Here is the reproducer script:

```python
import pytest
import os

def test_reproducer():
    param1 = '5\n10\n'
    param2 = '-16\n'

    pytest.main(['-k', f'test_solution[{param1}{param2}]'])

if __name__ == '__main__':
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed. Exiting with code 0.")
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

You can run this script with `python3 reproducer.py` to reproduce the issue.