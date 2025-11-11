Here is the reproducer script:

```python
import os
import sys
from io import StringIO
from subprocess import run, PIPE

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
    source_code = """
import pylint
print(pylint.__file__)
"""
    process = run(['python3', '-c', source_code], stdout=PIPE, stderr=PIPE)
    output, error = process.stdout.decode('utf-8').strip(), process.stderr.decode('utf-8').strip()
    if os.path.exists('.pylint'):
        raise AssertionError("Pylint stat file created in the current working directory")
    else:
        print("Issue not reproduced. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
```