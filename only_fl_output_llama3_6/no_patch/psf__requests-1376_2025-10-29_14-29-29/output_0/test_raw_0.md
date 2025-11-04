Here is the reproducer script:

```python
import requests
import httpbin
from unittest import TestCase

def test_unicode_multipart_post_fieldnames():
    r = requests.Request(method='POST',
                         url=httpbin('post'),
                         data={'stuff'.encode('utf-8'): 'elixr'},
                         files={'file': ('test_requests.py',
                                         open(__file__, 'rb'))})
    prep = r.prepare()
    assert not b'name="b\'stuff\'"' in prep.body, "Issue present"

try:
    test_unicode_multipart_post_fieldnames()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.