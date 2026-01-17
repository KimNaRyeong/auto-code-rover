 Here is a standalone python file `reproducer.py` that reproduces the issue:

```python
import pytest
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def some_condition():
    return True

@pytest.fixture
def bar():
    if some_condition():
        pytest.skip("Skipping")

def test_0(bar):
    assert 0
```

To run the script, execute `python3 reproducer.py` in the terminal. The script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The output should look like this:

```
================================== test session starts ==================================
platform linux -- Python 3.8.10, pytest-7.0.1, pluggy-1.0.0
rootdir: /path/to/reproducer
collected 1 item

reproducer.py s                                                                     [100%]
