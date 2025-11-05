Here is the reproducer script:

```python
import requests
from io import BytesIO
from unittest import TestCase
from urllib.parse import urlparse

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

class Reproducer(TestCase):
    def test_reproducer(self):
        url = "https://httpbin.org/json"
        response = requests.get(url, stream=True)
        
        self.assertEqual(response.status_code, 200)
        
        for chunk in response.iter_content(16*1024, decode_unicode=True):
            if not chunk:
                break
        else:
            with BytesIO() as f:
                f.write(chunk)
                content = f.getvalue().decode('utf-8')
                print(content)

        self.assertEqual(response.text, content)

if __name__ == "__main__":
    try:
        Reproducer().test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed. No issue found.")
        exit(0)
```

This script will make a GET request to the provided URL, then iterate over the response content using `iter_content` with `decode_unicode=True`. It will also get the text of the response and compare it to the decoded bytes from `iter_content`. If the two are not equal, an `AssertionError` will be raised.