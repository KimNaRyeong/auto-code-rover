Here is the reproducer script `reproducer.py`:

```python
import os
from django.core.files.storage import FileSystemStorage
from tempfile import NamedTemporaryFile

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
    from django.core.files.storage import FileSystemStorage
    fs = FileSystemStorage()
    with NamedTemporaryFile() as temp:
        temp_path = temp.name
        os.chmod(temp_path, 0o644)  # Set permissions to 0o644
        fs.save('test.txt', open(temp_path, 'rb'))
        file_perm = oct(os.stat(temp_path).st_mode)[-3:]
        if file_perm != '0o644':
            raise AssertionError(f"Expected permission 0o644 but got {file_perm}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before importing Django's FileSystemStorage. This should allow the script to reproduce the issue by setting the permissions of a temporary file and then checking its permissions.