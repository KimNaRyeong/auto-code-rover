Here is the reproducer script:

```python
import os
from tempfile import NamedTemporaryFile
import django
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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'  # Set the settings module
    django.setup()  # Initialize Django

    fs = FileSystemStorage()
    with NamedTemporaryFile() as temp:
        temp_path = temp.name
        os.chmod(temp_path, 0o644)  # Set permissions to 0o644
        fs.save('test.txt', open(temp_path, 'rb'))
        try:
            assert os.stat(temp_path).st_mode & 0o666 == 0o644
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable and initializes Django before running the reproducer.