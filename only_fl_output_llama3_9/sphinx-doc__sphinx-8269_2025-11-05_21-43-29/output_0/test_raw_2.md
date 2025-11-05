Here is the reproducer script:

```python
import os
import subprocess
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    os.chdir('path_to_your_project')  # replace with your project path
    try:
        subprocess.run(['make', 'linkcheck'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        if "404 Client Error: Not Found" not in str(e.stderr.decode('utf-8')):
            raise AssertionError("Issue reproduced")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script changes the directory to your project, runs the `make linkcheck` command and checks if the output contains "404 Client Error: Not Found". If not, it raises an `AssertionError`.