Here is the reproducer script:

```python
import os
import subprocess
from functools import partial

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
    sphinx_build_path = 'sphinx-build'
    if not os.path.exists(sphinx_build_path):
        raise AssertionError("Sphinx build command not found")

    try:
        subprocess.run([sphinx_build_path, "-j", "auto", "-n", "-b", "html", "-d", "build/doctrees", "-q", "-E", ".", "build/html"], check=True)
    except subprocess.CalledProcessError as e:
        raise AssertionError("Issue reproduced") from e
    else:
        print("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script checks if the `sphinx-build` command exists before running it. If the command does not exist, it raises an `AssertionError`.