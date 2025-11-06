Here is the reproducer script:

```python
import os
import sys
from subprocess import Popen, PIPE

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
    try:
        process = Popen(['python', 'manage.py', 'runserver'], stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        if b'<!DOCTYPE html>' in output and process.returncode == 0:
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script runs the `runserver` command using the subprocess module, captures its output and error streams, and checks if the output contains the expected HTML content. If it does and the process returned successfully (0), it raises an AssertionError to indicate that the issue is present.