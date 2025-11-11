Here is the `reproducer.py` script to reproduce the issue:
```
import os
import subprocess
from tempfile import TemporaryDirectory

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

with TemporaryDirectory() as tmpdir:
    os.chdir(tmpdir)
    subprocess.run(['sphinx-quickstart', '--project', 'proj', '--sep', '--author', 'me', '--release', '1.0', '--language', 'en'])
    with open('source/index.rst', 'a') as f:
        f.write('\n`foo <https://google.com/test.txt#test>`_')
    subprocess.run(['make', 'linkcheck'])

    with open('linkcheck/output.txt', 'r') as f:
        output = f.read()
        if 'Anchor \'test\' not found' in output:
            raise AssertionError("Issue is present: linkcheck reports Anchor not found instead of HTTP error")
        elif '404 Client Error: Not Found for url: https://google.com/test.txt' not in output:
            raise AssertionError("Issue is present: linkcheck does not report HTTP error")

print("Issue is fixed.")
```
This script creates a temporary directory, runs `sphinx-quickstart` to create a new project, appends the problematic link to `source/index.rst`, and then runs `make linkcheck`. It then checks the output of `linkcheck` to see if it reports an Anchor not found error instead of an HTTP error. If it does, it raises an `AssertionError` with a stack trace. If not, it prints "Issue is fixed."