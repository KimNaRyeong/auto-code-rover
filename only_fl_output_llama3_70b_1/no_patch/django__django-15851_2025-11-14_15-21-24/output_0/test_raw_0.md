Here is the `reproducer.py` file that reproduces the issue:
```
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

def main():
    try:
        # Reproduce the issue
        command = ["psql", "some_database", "--", "-c", "select * from some_table;"]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        if b"warning: extra command-line argument" in output:
            raise AssertionError("Issue is present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script runs the `psql` command with the arguments specified in the issue description, and checks if the output contains the warning message indicating that the extra command-line arguments are ignored. If it does, it raises an `AssertionError`. The `print_stacktrace` function is used to print a detailed stack trace of the error.

You can run this script using `python3 reproducer.py`, and it should raise an `AssertionError` if the issue is present, or exit with code 0 if the issue is fixed.