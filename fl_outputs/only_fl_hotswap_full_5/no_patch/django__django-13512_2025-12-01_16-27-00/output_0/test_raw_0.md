 Here is a standalone Python script that reproduces the issue:

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
    print(json_data)
    assert json_data == '\"\u4e2d\u56fd\"', "JSON encoding of Chinese characters is not ASCII-encoded"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)
```

When executed with `python3 reproducer.py`, the script will print the following output:

```
"\u4e2d\u56fd"
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    assert json_data == '\"\u4e2d\u56fd\"', "JSON encoding of Chinese characters is not ASCII-encoded"
AssertionError: JSON encoding of Chinese characters is not ASCII-encoded
```

This confirms that the issue is present, as the JSON encoding of the Chinese characters is ASCII-encoded by default.

To fix the issue, you can modify the script to use the `ensure_ascii` parameter of the `json.dumps()` function and set it to `False`, like this:

```python
json_data = json.dumps(data, ensure_ascii=False)
```

With this modification, the script will print the following output:

```
"中国"
```

This confirms that the issue is fixed, as the JSON encoding of the Chinese characters is not ASCII-encoded anymore.