To write a standalone Python script named `reproducer.py` that aims to reproduce the reported issue with `pylint` not respecting the `--ignore`, `--ignore-paths`, or `--ignore-patterns` options in `--recursive=y` mode, you can use this script:

```python
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

def setup_files():
    with open("bar.py", "w") as f:
        f.write("# import re\n")
    with open(".a_ignore.py", "w") as f:
        f.write("# This should be ignored\n")

def run_pylint_with_ignore(ignore_option, ignore_value):
    ignore_arg = f"{ignore_option}={ignore_value}" if ignore_value else ""
    command = ["pylint", "--recursive=y", "."] + [ignore_arg] if ignore_arg else []
    result = subprocess.run(command, capture_output=True, text=True)
    return result

def check_output_for_ignored_file(output, filename):
    return filename not in output

def main():
    setup_files()
    failed_checks = []

    tests = [
        ("--ignore", ".a_ignore.py"),
        ("--ignore-patterns", "^\.a_"),
        ("--ignore-paths", ".a_ignore.py"),
    ]

    for ignore_option, ignore_value in tests:
        result = run_pylint_with_ignore(ignore_option, ignore_value)
        if not check_output_for_ignored_file(result.stdout + result.stderr, ".a_ignore.py"):
            failed_checks.append(f"{ignore_option}={ignore_value}")

    if failed_checks:
        raise AssertionError(f"Pylint did not respect ignore options: {','.join(failed_checks)}")
    else:
        print("Test succeeded, pylint ignored the specified files.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    sys.exit(0)
```

**Explanation**:
1. **Setup**: The script creates two Python files, `bar.py` and `.a_ignore.py`, simulating a situation where `pylint` should ignore one of them based on the provided ignore options.
2. **Running Pylint**: It defines a function `run_pylint_with_ignore` that executes `pylint` with specified ignore options and captures its output.
3. **Check Output**: The function `check_output_for_ignored_file` verifies if the specified filename is present in `pylint` output to determine if it was ignored.
4. **Main Logic**: Iterates over different ignore options, running `pylint` for each, checking if the file supposed to be ignored was indeed ignored. A failed test indicates that `pylint` did not respect the ignore option as expected.
5. **Error Handling**: If any of the checks fail, it raises an `AssertionError`. If the script encounters an unexpected error, it prints a stack trace using the provided `print_stacktrace` function.

This script is designed to be self-contained and provides detailed feedback in case of failure, matching your criteria for demonstrating and troubleshooting the original issue.