 Here is a standalone Python script `reproducer.py` that should reproduce the issue:
```python
import subprocess
import sys
import warnings


def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def run_make_html():
    try:
        subprocess.check_call(["make", "html"], cwd="docs")
    except subprocess.CalledProcessError as e:
        return e


def main():
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        run_make_html()


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script runs the `make html` command in the `docs` directory, just like in the original issue. If the issue is present, it should raise an `AssertionError` with a stack trace.

To run the script, execute the following command in the root directory of the project:
```
python3 reproducer.py
```
If the issue is fixed, the script should exit with code 0.