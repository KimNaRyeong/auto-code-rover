Here is the reproducer script:

```python
import requests
import httpbin
import os

def test_unicode_multipart_post_fieldnames():
    r = requests.Request(method='POST',
                         url=httpbin('post'),
                         data={'stuff'.encode('utf-8'): 'elixr'},
                         files={'file': ('test_requests.py',
                                         open(os.path.abspath(__file__), 'rb'))})
    prep = r.prepare()
    assert not b'name="b\'stuff\'"' in prep.body, "AssertionError: True is not False"

try:
    test_unicode_multipart_post_fieldnames()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed. No AssertionError raised.")
exit(0)
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace of the error. If the issue is fixed, it will print "Test passed. No AssertionError raised." and exit with code 0.