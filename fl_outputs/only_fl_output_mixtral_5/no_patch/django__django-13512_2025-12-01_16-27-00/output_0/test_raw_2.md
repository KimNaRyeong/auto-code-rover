 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import json
import sys

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    data = '中国'
    json_data = json.dumps(data)
    assert json_data == u'"\u4e2d\u56fd"', "JSON encoding of Chinese characters is not ASCII"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
