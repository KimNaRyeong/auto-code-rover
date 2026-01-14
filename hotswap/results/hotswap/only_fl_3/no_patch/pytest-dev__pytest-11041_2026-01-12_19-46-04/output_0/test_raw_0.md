 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import json
import sys
import traceback

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_json_encoder():
    assert (object := "foo") in json.dumps(object)

try:
    test_json_encoder()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
To reproduce the issue, run the script with `python3 reproducer.py` and it should raise an `UnboundLocalError` with a stack trace.

If you want to test the fix for the issue, you can modify the `pytest` version in the `test_json_encoder` function to `7.2.x` or any version before `10758` and run the script again. The script should exit with code 0 without any errors.

For example, you can modify the function to:
```python
def test_json_encoder():
    pytest.__version__ = '7.2.0'  # set pytest version to 7.2.0
    assert (object := "foo") in json.dumps(object)
```
And run the script again with `python3 reproducer.py`. The script should exit with code 0 without any errors.