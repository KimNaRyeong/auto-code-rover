Here is a standalone `reproducer.py` script to reproduce the issue:
```
#!/usr/bin/env python3
import io
import requests
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

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

def main():
    contents = io.StringIO("." * (1024 * 1024 * 3))
    uploaded_file = InMemoryUploadedFile('docfile', 'bogus.txt\0', 'text/plain', len(contents.getvalue()), contents)
    try:
        # This should raise a ValueError
        uploaded_file.name
        assert False, "Issue is not present"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    main()
```
This script creates an `InMemoryUploadedFile` instance with a filename containing a null byte and tries to access its `name` attribute. If the issue is present, this should raise a `ValueError` due to the embedded null byte.

If the issue is present, the script will raise an `AssertionError` with a stack trace of the error. If the issue is fixed, the script will exit with code 0.

To run the script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.