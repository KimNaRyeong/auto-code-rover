Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import requests
import os

def test_unicode_multipart_post_fieldnames():
    try:
        r = requests.Request(method='POST',
                             url='https://httpbin.org/post',
                             data={'stuff'.encode('utf-8'): 'elixr'},
                             files={'file': ('test_requests.py', open(__file__, 'rb'))})
        prep = r.prepare()
        assert b'name="stuff"' in prep.body
        assert not b"name=b'stuff'" in prep.body
    except AssertionError as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e: Exception):
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

if __name__ == '__main__':
    test_unicode_multipart_post_fieldnames()
```
This script should reproduce the issue and raise an `AssertionError` with a stack trace when the issue is present. If the issue is fixed, it will exit with code 0.

Please note that I've kept the same code as before, but if you want to try a different approach, please let me know and I'll be happy to help.