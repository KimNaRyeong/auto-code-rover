```python
# reproducer.py

import requests


def httpbin(endpoint):
    """Construct httpbin URL."""
    return f'https://httpbin.org/{endpoint}'


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


def test_unicode_multipart_post_fieldnames():
    try:
        r = requests.Request(method='POST',
                             url=httpbin('post'),
                             data={b'stuff': 'elixr'},  # Encoding moved here for clarity
                             files={'file': ('test_requests.py', open(__file__, 'rb'))})
        prep = r.prepare()
        assert b'name="stuff"' in prep.body, "Field name not correctly encoded in the body"
        assert not b'name="b\'stuff\'"' in prep.body, "Field name incorrectly double-encoded"
    except AssertionError as e:
        print_stacktrace(e)
        raise


if __name__ == "__main__":
    test_unicode_multipart_post_fieldnames()
```