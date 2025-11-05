Here is the reproducer script:

```python
import os
from tempfile import NamedTemporaryFile
from django.core.files.storage import FileSystemStorage

def main():
    fs = FileSystemStorage()
    with NamedTemporaryFile() as temp:
        temp_path = temp.name
        fs.save('test.txt', open(temp_path, 'rb'))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    os.chmod('test.txt', 0o644)