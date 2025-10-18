```python
import os
import subprocess
import sys
from typing import List


def setup_test_environment() -> None:
    os.makedirs('.a', exist_ok=True)
    with open('.a/foo.py', 'w') as f:
        f.write('# import re\n')
    with open('bar.py', 'w') as f:
        f.write('# import re\n')


def run_pylint_command(command: List[str]) -> str:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )
    stdout, stderr = process.communicate()
    if process.returncode not in (0, 16, 20, 24, 28, 32):
        # Pylint exit codes 0, and any combination of 1, 2, 4, 8, 16 for different issue types
        raise Exception(f"Pylint execution failed with code {process.returncode}: {stderr}")
    return stdout + stderr


def test_ignore_functionality() -> None:
    setup_test_environment()

    commands = [
        ['pylint', '--recursive=y', '.'],
        ['pylint', '--recursive=y', '--ignore=.a', '.'],
        ['pylint', '--recursive=y', '--ignore-paths=.a', '.'],
        ['pylint', '--recursive=y', '--ignore-patterns=^\\.a', '.']
    ]

    for command in commands:
        output = run_pylint_command(command)
        if ".a/foo.py" in output:
            raise AssertionError(f"'foo.py' should be ignored by command: {' '.join(command)}")


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
        test_ignore_functionality()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issues detected.")
        sys.exit(0)


if __name__ == '__main__':
    main()
```

This script, when placed in the root directory of the project and executed, sets up a test environment by creating files expected to trigger the issue with Pylint's `--ignore`, `--ignore-paths`, and `--ignore-patterns` configurations in recursive mode. It then runs a series of `pylint` commands designed to test whether these ignore configurations are respected. If the bug is present, an `AssertionError` is raised, and a stack trace is printed; otherwise, it reports no issues detected. This script thereby facilitates automated verification of the bug's fix or presence.