Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import requests
import httpbin
import unittest

def test_unicode_multipart_post_fieldnames():
    r = requests.Request(method='POST',
                         url=httpbin('post'),
                         data={'stuff'.encode('utf-8'): 'elixr'},
                         files={'file': ('test_requests.py',
                                         open(__file__, 'rb'))})
    prep = r.prepare()
    assert not b'name="b\'stuff\'"' in prep.body, "AssertionError: True is not false"

if __name__ == '__main__':
    try:
        test_unicode_multipart_post_fieldnames()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def print_stacktrace(e):
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

```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.