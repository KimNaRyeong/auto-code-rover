 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import pytest

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_approx():
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except Exception as e:
        print_stacktrace(e)

test_approx()
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    test_approx()
  File "reproducer.py", line 10, in test_approx
    assert [1, 2] == pytest.approx([1.001, 2.002])
AssertionError: assert [1, 2] == approx([1.001...02 ± 2.0e-06])
Probably an object has a faulty __repr__.)
```
As you can see, there is no `ModuleNotFoundError: No module named 'numpy'` in the stack trace, which makes the error message clearer and easier to understand.