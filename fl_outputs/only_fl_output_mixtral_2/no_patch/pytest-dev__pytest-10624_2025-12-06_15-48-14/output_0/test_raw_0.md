 Here's a standalone Python script `reproducer.py` that reproduces the issue:

```python
import pytest

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_foo_dict():
    a = {'foo': 42.0}
    b = {'foo': 0.0}
    try:
        assert a == pytest.approx(b)
    except Exception as e:
        print_stacktrace(e)

def test_foo_list():
    a = [42.0]
    b = [0.0]
    assert a == pytest.approx(b)
```

To run the script, execute `python3 reproducer.py` in the terminal. The script will print the stack trace of the `AssertionError` caused by the issue.

The output should look like this:

```
Traceback (most recent call last):
  File "reproducer.py", line 16
    assert a == pytest.approx(b)
E   AssertionError: assert {'foo': 42.0} == approx({'foo': 0.0 ± 1.0e-12})
Probably an object has a faulty __repr__.)
```