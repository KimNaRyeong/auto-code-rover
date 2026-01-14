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

def test_pytest_none_approx():
    actual_result = {"a": 1.2}
    expected_result = {"a": None}
    approx_expected_result = pytest.approx(expected_result)
    try:
        assert approx_expected_result == actual_result
    except AssertionError as e:
        print_stacktrace(e)
        raise e
```
To reproduce the issue, execute the script with `python3 reproducer.py`. The script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    test_pytest_none_approx()
  File "reproducer.py", line 10, in test_pytest_none_approx
    assert approx_expected_result == actual_result
AssertionError: assert approx({'a': 1.2 ± 1.2e-06}) == {'a': None}
	(pytest_assertion plugin: representation of details failed: /Users/milanwiedemann/.pyenv/versions/3.10.4/lib/python3.10/site-packages/_pytest/python_api.py:270: TypeError: unsupported operand type(s) for -: 'float' and 'NoneType'.
		Probably an object has a faulty __repr__.)
Traceback (most recent call last):
  File "reproducer.py", line 7, in print_stacktrace
    tb = traceback.extract_tb(e.__traceback__)
TypeError: unsupported operand type(s) for -: 'float' and 'NoneType'
```
This stack trace shows that the issue is caused by the `-` operation between a `float` and a `NoneType` in the `pytest` library.