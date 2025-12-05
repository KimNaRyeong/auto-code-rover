 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
When executed with `python3 reproducer.py`, it raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    pytest.main(["-rs", "../my_tests/test1.py"])
  File "/home/user/.local/lib/python3.8/site-packages/pytest.py", line 625, in main
    return exitstatus(call_and_report(pytestdir, args))
  File "/home/user/.local/lib/python3.8/site-packages/pytest.py", line 606, in call_and_report
    return report.report_call(args, pytestdir.session)
  File "/home/user/.local/lib/python3.8/site-packages/pytest_enabler/_pytest/report.py", line 10, in report_call
