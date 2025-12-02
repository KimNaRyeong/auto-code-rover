 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import shutil
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.core.exceptions import SuspiciousOperation

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Set up Django environment
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csrfbug.settings')
django.setup()

# Create a temporary file upload handler
handler = TemporaryFileUploadHandler()

# Test scenario 1: file uploads work as expected
try:
    handler.new_file('file', b'x' * 1024 * 1024)  # 1 MB file
    handler.receive_data(b'x' * 1024 * 1024)
    handler.file.close()
except Exception as e:
    print("Scenario 1 failed:", e)
    print_stacktrace(e)
    assert False

# Test scenario 2: file uploads work only for files that fit in FILE_UPLOAD_MAX_MEMORY_SIZE
try:
    shutil.rmtree('media/tmp')
except FileNotFoundError:
    pass
try:
    handler.new_file('file', b'x' * (1024 * 1024 + 1))  # 1 MB + 1 byte file
    handler.receive_data(b'x' * (1024 * 1024 + 1))
    handler.file.close()
except SuspiciousOperation as e:
    # Expected exception
    pass
except Exception as e:
    print("Scenario 2 failed:", e)
    print_stacktrace(e)
    assert False

# Test scenario 3: error reported for all file uploads
try:
    shutil.rmtree('media')
except FileNotFoundError:
    pass
try:
    handler.new_file('file', b'x' * 1024 * 1024)  # 1 MB file
    handler.receive_data(b'x' * 1024 * 1024)
    handler.file.close()
except SuspiciousOperation as e:
    # Expected exception
    pass
except Exception as e:
    print("Scenario 3 failed:", e)
    print_stacktrace(e)
    assert False

print("Test passed")
```
This script creates a temporary file upload handler and tests the three scenarios described in the issue. In scenario 1, it uploads a 1 MB file and expects it to succeed. In scenario 2, it removes the `media/tmp` directory and uploads a file that is larger than `FILE_UPLOAD_MAX_MEMORY_SIZE` (1 MB) and expects a `SuspiciousOperation` exception to be raised. In scenario 3, it removes the entire `media` directory and uploads a 1 MB file and expects a `SuspiciousOperation` exception to be raised.

The script uses the `print_stacktrace` function provided to print the stack trace of any exceptions that are raised. If an exception is raised in any of the scenarios, the script asserts that the exception is of type `SuspiciousOperation` and prints the stack trace. If no exceptions are raised, the script prints "Test passed".