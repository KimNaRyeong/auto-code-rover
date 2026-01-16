Below is a standalone Python script `reproducer.py` designed to validate whether the `pylint` bug related to ignoring `ignore-paths` when using the `--recursive=y` option is present or fixed. The script programmatically calls `pylint` on a sample directory structure within the project, checking for linting errors in files that should be ignored according to the `ignore-paths` configuration. If errors are found in the ignored paths, it raises an `AssertionError`, demonstrating the presence of the bug. If no such errors are found (indicating the issue is fixed), it exits with code 0, implying success.

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


def check_pylint_output(output):
    # This function checks if pylint's output contains any issues within ignored paths
    ignored_files_prefix = "src/gen/"
    for line in output.split('\n'):
        if line.startswith("************* Module"):
            file_path = line.split(" ")[-1]
            if file_path.replace("\\", "/").startswith(ignored_files_prefix):
                return False
    return True

def run_pylint():
    # Creating the necessary directory structure and files
    os.makedirs("src/gen", exist_ok=True)
    with open("src/gen/test_file.py", "w") as test_file:
        test_file.write("# This file should be ignored by pylint\n")
    
    with open("pyproject.toml", "w") as config_file:
        config_content = """
[tool.pylint.MASTER]
ignore-paths = [
  # Auto generated
  "^src/gen/.*$",
]
"""
        config_file.write(config_content)

    # Running pylint programmatically
    try:
        result = subprocess.run(["pylint", "--recursive=y", "src/"],
                                capture_output=True, text=True, check=True)
        output = result.stdout + result.stderr

        assert check_pylint_output(output), "Ignored files are being linted!"

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Clean up created files and directories for cleanliness
        os.remove("pyproject.toml")
        os.remove("src/gen/test_file.py")
        os.rmdir("src/gen")
        os.rmdir("src")

if __name__ == "__main__":
    run_pylint()
    print("No issues found in ignored paths. The bug seems to be fixed.")
    sys.exit(0)
```

This script does the following:
- Sets up a minimal project structure with a directory and file that should be ignored according to the `ignore-paths` set in `pyproject.toml`.
- Runs `pylint` on this structure with the `--recursive=y` option.
- Checks the output from `pylint` for any linting errors related to the ignored file.
- Raises an `AssertionError` and prints a stack trace if errors from the ignored file are detected (indicating the bug is present).
- Cleans up the project structure by deleting created files and directories.