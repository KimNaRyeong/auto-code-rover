Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import subprocess
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_reproducer(self):
        try:
            os.makedirs('.a')
            with open('.a/foo.py', 'w') as f:
                f.write('# import re\n')

            commands = [
                ['pylint', '--recursive=y', '.'],
                ['pylint', '--recursive=y', '--ignore=.a', '.'],
                ['pylint', '--recursive=y', '--ignore-paths=.a', '.'],
                ['pylint', '--recursive=y', '--ignore-patterns="^\.a"', '.']
            ]

            for command in commands:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                if "Disallowed name" in str(output.decode()):
                    raise AssertionError("Pylint did not respect the ignore setting")
        except Exception as e:
            print_stacktrace(e)

if __name__ == '__main__':
    Reproducer().test_reproducer()
```

This script creates the necessary directories and files, runs the Pylint commands, and checks if any of them raise an error. If an error is raised, it prints a stack trace using the provided `print_stacktrace` function.