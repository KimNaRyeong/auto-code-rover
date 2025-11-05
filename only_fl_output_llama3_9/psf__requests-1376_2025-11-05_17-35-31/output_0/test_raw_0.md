Here is the reproducer script:

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
    if b'name="b\'stuff\'' in prep.body:
        raise AssertionError("Expected False, got True")

try:
    test_unicode_multipart_post_fieldnames()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an AssertionError and print a stack trace.