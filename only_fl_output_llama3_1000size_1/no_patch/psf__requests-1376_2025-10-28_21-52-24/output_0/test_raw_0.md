Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import requests
import httpbin
import sys

def test_unicode_multipart_post_fieldnames():
    r = requests.Request(method='POST',
                         url=httpbin('post'),
                         data={'stuff'.encode('utf-8'): 'elixr'},
                         files={'file': ('test_requests.py',
                                         open(__file__, 'rb'))})
    prep = r.prepare()
    assert not b'name="b\'stuff\'"' in prep.body

try:
    test_unicode_multipart_post_fieldnames()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. When the issue is fixed, it will exit with code 0.