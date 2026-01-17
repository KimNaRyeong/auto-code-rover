Here's how you could write a `reproducer.py` Python script to verify whether the issue with `pylint --recursive=y` not respecting `ignore-paths` from `pyproject.toml` is occurring. This script dynamically creates a minimal project layout with necessary files, runs `pylint` on this setup, and checks whether files in the ignored path are being linted.

```python
import subprocess
import os
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


def setup_project_structure():
    os.makedirs("src/gen", exist_ok=True)
    with open("src/gen/ignored_file.py", "w") as f:
        f.write("# This file should be ignored by pylint\n")

    with open("src/checked_file.py", "w") as f:
        f.write("# This file should be checked by pylint\n")

    with open("pyproject.toml", "w") as f:
        f.write("""
[tool.pylint.MASTER]
ignore-paths = [
  # Auto generated
  "^src/gen/.*$",
]
""")


def run_pylint():
    try:
        result = subprocess.run(["pylint", "--recursive=y", "src/"], capture_output=True, text=True, check=True)
        assert "ignored_file.py" not in result.stdout, "The ignored file was checked by pylint"
        print("Ignored paths are respected. No issues found.")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError("Pylint did not respect the ignore-paths configuration.") from e
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(e)


def main():
    setup_project_structure()
    run_pylint()
    cleanup_project_structure()


def cleanup_project_structure():
    os.remove("src/gen/ignored_file.py")
    os.remove("src/checked_file.py")
    os.rmdir("src/gen")
    os.rmdir("src")
    os.remove("pyproject.toml")


if __name__ == "__main__":
    main()
```

This script does the following:
- Sets up a simple project directory with a `src/gen` directory that should be ignored according to the `pyproject.toml`.
- It runs `pylint` over the `src` directory using the `--recursive=y` option.
- It checks the output of `pylint` for occurrences of `ignored_file.py` to verify if `pylint` respected the `ignore-paths` directive.
- An assertion error is raised if the issue is present, causing `pylint` to lint the ignored file.
- Cleans up the created files and directories after the check.

For this script to work, ensure `pylint` and necessary dependencies are installed in your environment and that this script is executed in a writable directory where it can create and delete files/directories.