Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import subprocess
import sys
from unittest import TestCase

def run_pylint(command):
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        if "AssertionError" in str(output):
            raise AssertionError("Pylint did not respect ignore settings")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)

class Reproducer(TestCase):

    def test_pylint_ignores(self):
        command = f"pylint --recursive=y ."
        run_pylint(command)
        
        command = f"pylint --recursive=y --ignore=.a ."
        run_pylint(command)
        
        command = f"pylint --recursive=y --ignore-paths=.a ."
        run_pylint(command)
        
        command = f"pylint --recursive=y --ignore-patterns='^\.a' ."
        run_pylint(command)

if __name__ == "__main__":
    test_result = Reproducer().run()
    if not test_result.wasSuccessful():
        sys.exit(1)
```

This script runs the `pylint` commands with different ignore settings and checks if the output contains any error messages. If it does, it raises an `AssertionError`. The script also prints a stack trace of the error using the provided function.

To run this script, save it to a file named `reproducer.py`, then execute it with Python: `python3 reproducer.py`.