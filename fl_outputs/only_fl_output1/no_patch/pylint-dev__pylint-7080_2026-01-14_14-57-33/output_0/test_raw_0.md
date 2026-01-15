To reproduce the issue described, we'll write a `reproducer.py` script that mimics your project structure and attempts to run `pylint` in a way that should respect the `ignore-paths` configuration. The script will then assert whether files expected to be ignored were indeed skipped by `pylint`. For this reproducer to be fully automated, it relies on dynamically creating the necessary files, running `pylint`, and parsing its output to determine if the issue is present.

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

def run_pylint():
    try:
        subprocess.run(["pylint", "--recursive=y", "src/"], check=True, capture_output=True, text=True)
        print("Pylint ran successfully, expected ignored files check next.")
    except subprocess.CalledProcessError as e:
        output = e.stdout + e.stderr
        if "src/gen/" in output:
            raise AssertionError("Pylint checked files that should have been ignored.") from e
        else:
            print("Pylint did not check ignored files, as expected.")

def main():
    os.makedirs("src/gen", exist_ok=True)

    with open("pyproject.toml", "w") as config_file:
        config_file.write("""
[tool.pylint.MASTER]
ignore-paths = [
  # Auto generated
  "^src/gen/.*$",
]
""")

    # Create a dummy Python file in the should-be-ignored path
    with open("src/gen/ignored_file.py", "w") as ignored_file:
        ignored_file.write("# This file should be ignored by pylint\n")

    with open("src/main.py", "w") as main_file:
        main_file.write("# Main application file\n")

    try:
        run_pylint()
    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not present or fixed. No AssertionError raised.")

if __name__ == "__main__":
    main()
```

This script works as follows:
- It sets up a project structure with a `src/gen/` directory intended to be ignored according to the `pyproject.toml` configuration.
- It then writes a minimal `pyproject.toml` with the `ignore-paths` configuration targeting `src/gen/.*`.
- Two Python files are created: one in the `src/gen/` directory (`ignored_file.py`) and another outside it (`main.py`), to check if `pylint` will indeed ignore the former but not the latter.
- It runs `pylint` with `--recursive=y` option targeting the `src/` directory.
- If `pylint` attempts to check the content of `src/gen/ignored_file.py`, it's considered an unsuccessful run, raising an `AssertionError`.
- If no such error occurs, the script assumes the issue is either not present or fixed.

Remember, for this script to run correctly, you'll need the `pylint` package installed in your environment. You might want to adapt the script based on the detailed setup of your actual project or environment.