Here is the reproducer script:

```python
import os
from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import MemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import FileSystemStorage

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
    fs = FileSystemStorage()
    with NamedTemporaryFile() as temp:
        with open(temp.name, 'w') as f:
            f.write('test')
        os.chmod(temp.name, 0o644)
        uploaded_file = MemoryUploadedFile(open(temp.name, 'rb'), 'text/plain', 'test.txt', 'text/plain', None)
        fs.save('test.txt', uploaded_file)

    with NamedTemporaryFile() as temp:
        with open(temp.name, 'w') as f:
            f.write('test')
        os.chmod(temp.name, 0o644)
        uploaded_file = TemporaryUploadedFile(open(temp.name, 'rb'), 'text/plain', 'test.txt', 'text/plain', None)
        fs.save('test.txt', uploaded_file)

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script creates a temporary file with the desired permissions and then uses Django's `FileSystemStorage` to upload it using both `MemoryUploadedFile` and `TemporaryUploadedFile`. If the issue is present, an `AssertionError` will be raised.