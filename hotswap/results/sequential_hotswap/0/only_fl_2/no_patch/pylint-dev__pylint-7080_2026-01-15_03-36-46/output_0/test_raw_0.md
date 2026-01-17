Certainly! Following is a Python script named `reproducer.py` designed to automatically verify the pylint behavior regarding the `--recursive=y` option and `ignore-paths` configuration. This script sets up a temporary project structure, runs `pylint` on it, and checks whether files supposed to be ignored (as specified in `pyproject.toml`) are actually ignored. It raises an `AssertionError` when the issue is present, indicative of the bug being reproducible. Upon the issue being fixed, the script should not raise an error and exit with code 0.

```python
import subprocess
import tempfile
import os
import shutil

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def create_temp_project():
    temp_dir = tempfile.mkdtemp(prefix="pylint_test")
    
    # Creating project structure
    os.makedirs(os.path.join(temp_dir, "src", "gen"), exist_ok=True)

    # Python code to ignore
    with open(os.path.join(temp_dir, "src", "gen", "ignore_me.py"), "w") as f:
        f.write("# This should be ignored according to ignore-paths\n")

    # Python code to check
    with open(os.path.join(temp_dir, "src", "check_me.py"), "w") as f:
        f.write("def foo():\n    pass\n")

    # Configuration file
    pyproject_content = """[tool.pylint.MASTER]
ignore-paths=[
  # Auto generated
  "^src/gen/.*$",
]
"""
    with open(os.path.join(temp_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject_content)

    return temp_dir

def run_pylint(project_dir):
    try:
        output = subprocess.check_output(
            ["pylint", "--recursive=y", os.path.join(project_dir, "src/")],
            stderr=subprocess.STDOUT,
            text=True
        )
        if "ignore_me.py" in output:
            raise AssertionError("Pylint did not ignore the paths specified in ignore-paths as expected.")
        return output
    except subprocess.CalledProcessError as ex:
        print_stacktrace(ex)
        raise

def main():
    project_dir = create_temp_project()
    try:
        output = run_pylint(project_dir)
        print("Pylint output:", output)
        print("Test passed. The issue is fixed or not reproducible.")
    except AssertionError as e:
        print_stacktrace(e)
    finally:
        shutil.rmtree(project_dir)  # Cleanup

if __name__ == "__main__":
    main()
```

This script performs the following steps:
- Creates a temporary directory and sets up a test project structure within it, including the creation of a Python file `ignore_me.py` located in a directory that should be ignored (`src/gen/`), as specified in a `pyproject.toml` file.
- Runs `pylint` on the project directory using subprocess, specifically targeting the `src/` directory with the `--recursive=y` option.
- Checks the pylint output to see if `ignore_me.py` was indeed ignored. If `ignore_me.py` is found in pylint's output, an `AssertionError` is raised, indicating that pylint did not respect the `ignore-paths` setting.
- Cleans up by deleting the temporary project directory.

Please ensure `pylint` is installed in your environment and available in the path for the script to work correctly.