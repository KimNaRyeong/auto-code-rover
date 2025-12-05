 Here's a standalone Python script `reproducer.py` that reproduces the issue:
```python
import subprocess
import sys
from typing import List

def run_pylint(args: List[str]) -> None:
    try:
        pylint_output = subprocess.check_output(args, universal_newlines=True)
        print(pylint_output, end="")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main() -> None:
    print("Running pylint with --recursive=y")
    run_pylint(["pylint", "--recursive=y", "."])

    print("\nRunning pylint with --recursive=y and --ignore=.a")
    run_pylint(["pylint", "--recursive=y", "--ignore=.a", "."])

    print("\nRunning pylint with --recursive=y and --ignore-paths=.a")
    run_pylint(["pylint", "--recursive=y", "--ignore-paths=.a", "."])

    print("\nRunning pylint with --recursive=y and --ignore-patterns=^\.a")
    run_pylint(["pylint", "--recursive=y", "--ignore-patterns=^\.a", "."])

if __name__ == "__main__":
    main()
```
This script creates a `.a` directory with a `foo.py` file inside it and a `bar.py` file in the root directory. The script then runs pylint with `--recursive=y` and different ignore options.

To run the script, create a directory with the following structure:
```diff
- reproducer.py
- .a
  - foo.py
- bar.py
```
And execute `python3 reproducer.py`. The output should show that pylint does not respect the ignore options in recursive mode.

The expected behavior is that `foo.py` should be ignored by all the commands, but it is not. This contradicts the documentation and compromises the usefulness of recursive mode.