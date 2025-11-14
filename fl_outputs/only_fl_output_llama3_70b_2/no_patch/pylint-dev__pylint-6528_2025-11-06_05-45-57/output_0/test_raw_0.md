Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import subprocess
import os

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

def main():
    # Create a directory with an ignored file
    os.makedirs('.a', exist_ok=True)
    with open(os.path.join('.a', 'foo.py'), 'w') as f:
        f.write('# import re\n')

    # Run pylint in recursive mode with and without ignore settings
    commands = [
        ['pylint', '--recursive=y', '.'],
        ['pylint', '--recursive=y', '--ignore=.a', '.'],
        ['pylint', '--recursive=y', '--ignore-paths=.a', '.'],
        ['pylint', '--recursive=y', '--ignore-patterns="^\.a"', '.']
    ]

    for command in commands:
        output = subprocess.check_output(command, universal_newlines=True)
        if 'Module foo' in output:
            raise AssertionError("Pylint did not respect ignore settings")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
```
This script creates a directory `.a` with an ignored file `foo.py`, runs pylint in recursive mode with and without ignore settings, and checks if the output contains the ignored module. If it does, it raises an `AssertionError`.