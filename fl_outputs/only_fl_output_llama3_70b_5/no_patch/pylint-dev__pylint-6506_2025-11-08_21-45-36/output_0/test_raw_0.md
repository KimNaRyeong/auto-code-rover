Here is the `reproducer.py` file that reproduces the issue:
```
python
import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    subprocess.run(["pylint", "-Q"], check=True)
except subprocess.CalledProcessError as e:
    output = e.stdout.decode("utf-8")
    if "Unrecognized option found: Q" in output and "Traceback (most recent call last):" in output:
        raise AssertionError("Pylint printed a traceback for an unrecognized option")
    else:
        print(output)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script runs `pylint -Q` and checks if the output contains both the error message "Unrecognized option found: Q" and a traceback. If it does, it raises an `AssertionError`. If not, it prints the output.