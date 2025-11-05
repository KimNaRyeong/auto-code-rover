Here is the reproducer script:

```python
import requests
from django.http.multipartparser import MultiPartParser
from django.core.files.uploadhandler import FakeFileUploadHandler

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

def reproduce_issue():
    data = {
        'file': ('测试.txt", text/plain; name="file"; filename*="UTF-8''%E6%B5%8B%E8%AF%95.txt"',
                 'test')
    }
    parser = MultiPartParser(FakeFileUploadHandler(), ['file'], 1024)
    for key, value in data.items():
        parser.feed(key + '=' + value[0])
    try:
        file_name = parser.get_file('file').name
        assert file_name == "测试.txt", f"Expected '测试.txt' but got '{file_name}'"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sends a POST request to Django's MultiPartParser with the given data and checks if the file name is correctly parsed. If not, it prints the stack trace of the assertion error and exits with code 1.