```python
import os
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

def setup_test_files():
    os.makedirs(".a", exist_ok=True)
    with open(".a/foo.py", "w") as f:
        f.write("# import re\n")
    with open("bar.py", "w") as f:
        f.write("# import re\n")

def run_pylint(ignore_option):
    try:
        result = subprocess.check_output(
            ["pylint", "--recursive=y", ignore_option, "."],
            stderr=subprocess.STDOUT,
            text=True
        )
        if ".a/foo.py" in result:
            raise AssertionError("Pylint did not respect ignore settings")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise

def main():
    setup_test_files()

    ignore_options = ["", "--ignore=.a", "--ignore-paths=.a", "--ignore-patterns=^\\.a"]

    try:
        for option in ignore_options:
            run_pylint(option)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Issue not present, pylint respected ignores in `--recursive=y` mode.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

When you run this script (`python3 reproducer.py`) in the root directory of the project, it will set up the test files as described in the issue and then run Pylint with the specified ignore options. If Pylint fails to respect the ignore configurations and checks the files/directories that it was supposed to ignore, the script raises an `AssertionError` and prints a traceback. This allows you to visually confirm and investigate the issue described. If the issue is fixed, the script exits normally indicating the problem is not present.