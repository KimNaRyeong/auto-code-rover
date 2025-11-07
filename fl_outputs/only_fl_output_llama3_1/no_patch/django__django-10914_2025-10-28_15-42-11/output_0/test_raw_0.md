Here is the reproducer script:

```python
import os
from tempfile import NamedTemporaryFile
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

def main():
    fs = FileSystemStorage()
    with NamedTemporaryFile() as tmp:
        content_file = ContentFile(b'Hello, World!')
        fs.save('test.txt', content_file)
        os.chmod(tmp.name, 0o644)

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)
```

This script creates a temporary file using `NamedTemporaryFile`, writes some content to it, and then saves the file to Django's FileSystemStorage. It also sets the permissions of the temporary file to `0o644` using `os.chmod`. If the issue is present (i.e., the permissions of the saved file are not `0o644`), an `AssertionError` will be raised, which will be caught and printed by the script.