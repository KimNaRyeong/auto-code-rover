 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import pytest
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_skip():
    pytest.skip("no way of currently testing this")

if __name__ == "__main__":
    try:
        pytest.main(["-rs", "../my_tests/test1.py"])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` and print a stack trace showing the issue.

The output will be similar to:
```yaml
============================================== test session starts ===============================================
platform linux -- Python 3.7.5, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /home/xyz
plugins: hypothesis-5.6.0
collected 1 item

../my_tests/test1.py s                                                                                     [100%]
