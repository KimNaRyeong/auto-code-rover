Here is the reproducer script:

```python
import requests
import httpbin
import unittest
from io import BytesIO
from urllib.parse import urlparse, urlunparse

def test_unicode_multipart_post_fieldnames():
    r = requests.Request(method='POST',
                         url=urlunparse((httpbin('post'), '', '', '', '')),
                         data={'stuff'.encode('utf-8'): 'elixr'},
                         files={'file': ('test_requests.py', BytesIO(b'content'))})
    prep = r.prepare()
    assert not b'name="b\'stuff\'"' in prep.body

if __name__ == '__main__':
    try:
        test_unicode_multipart_post_fieldnames()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script should be executed by `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.