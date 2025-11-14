Here is a standalone Python script `reproducer.py` to reproduce the issue:
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
    # Create a sample Python project with some lint errors
    os.makedirs('app', exist_ok=True)
    with open('app/main.py', 'w') as f:
        f.write("print('Hello, world!')\n")
        f.write("print('This is a test')\n")

    with open('pylintrc', 'w') as f:
        f.write("[MASTER]\n")
        f.write("jobs=1\n")

    # Run pylint with --jobs=1 and capture the output
    output1 = subprocess.check_output(['venv/bin/pylint', '--jobs=1', '--rcfile=pylintrc', 'app/main.py']).decode('utf-8')

    # Run pylint with --jobs=2 and capture the output
    output2 = subprocess.check_output(['venv/bin/pylint', '--jobs=2', '--rcfile=pylintrc', 'app/main.py']).decode('utf-8')

    # Check if the outputs are different
    if output1 != output2:
        raise AssertionError("Different output with --jobs=1 and --jobs=2")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
```
This script creates a sample Python project with some lint errors, runs pylint with `--jobs=1` and `--jobs=2`, captures the output, and checks if the outputs are different. If they are, it raises an `AssertionError`.