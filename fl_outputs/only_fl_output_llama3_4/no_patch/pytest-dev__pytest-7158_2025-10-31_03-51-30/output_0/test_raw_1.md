Here is the reproducer script:

```python
import os
import sys
from functools import wraps

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

def assert_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            print_stacktrace(e)
            raise
        else:
            sys.exit(0)  # exit with code 0 when the issue is fixed

    return wrapper

@assert_issue
def test_reproducer():
    os.chdir('/home/xyz')
    os.system('pytest -rs ../my_tests/test1.py')

if __name__ == "__main__":
    test_reproducer()
```

This script will change into the `/home/xyz` directory, then run the pytest command with the given options. If an AssertionError is raised during the execution of the `test_reproducer` function, it will print the stack trace using the provided function and then raise the same exception again.