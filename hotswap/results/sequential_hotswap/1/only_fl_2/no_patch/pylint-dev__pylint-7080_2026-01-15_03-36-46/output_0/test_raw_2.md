To create a `reproducer.py` that addresses the issue mentioned, we will simulate a smaller scale project and attempt to reproduce the problem where `pylint` does not respect `ignore-paths` from the `pyproject.toml` configuration when run with `--recursive=y`. If the issue is present, the script will raise an `AssertionError` explicitly indicating that files intended to be ignored were incorrectly processed.

This script will programmatically create a minimal project structure in a temporary directory, including a `pyproject.toml` with `ignore-paths` configuration pointing to a generated directory that should be ignored, and a Python script in both the ignored and checked paths. It will then run `pylint` on this structure and assert whether files in the ignored paths were still checked.

Please note, the script assumes `pylint` is installed and accessible in the environment where the script is run.

```python
import subprocess
import os
import tempfile
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

def setup_temp_project():
    temp_dir = tempfile.mkdtemp()
    src_dir = os.path.join(temp_dir, "src")
    gen_dir = os.path.join(src_dir, "gen")

    os.makedirs(gen_dir)

    ignored_script_path = os.path.join(gen_dir, "ignored.py")
    with open(ignored_script_path, "w") as f:
        f.write("# This file should be ignored by pylint\n")

    checked_script_path = os.path.join(src_dir, "checked.py")
    with open(checked_script_path, "w") as f:
        f.write("# This file should be checked by pylint\n")

    toml_content = """[tool.pylint.MASTER]
ignore-paths = ["^src/gen/.*$"]
"""
    toml_path = os.path.join(temp_dir, "pyproject.toml")
    with open(toml_path, "w") as f:
        f.write(toml_content)

    return temp_dir

def run_pylint(project_dir):
    try:
        pylint_cmd = ["pylint", "--recursive=y", os.path.join(project_dir, "src/")]
        process = subprocess.run(pylint_cmd, check=True, capture_output=True, text=True)
        output = process.stdout
        if "ignored.py" in output:
            raise AssertionError("pylint checked files that should have been ignored according to ignore-paths.")
        else:
            print("No AssertionError raised. pylint behavior is as expected.")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise

def main():
    project_dir = setup_temp_project()
    try:
        run_pylint(project_dir)
    finally:
        shutil.rmtree(project_dir)

if __name__ == "__main__":
    main()
```

This script:
- Creates a temporary directory to simulate a project structure
- Writes the `ignore-paths` configuration into a `pyproject.toml` file
- Creates a Python script in the ignored path (`src/gen/ignored.py`) and one outside it (`src/checked.py`)
- Runs `pylint` on this structure with `--recursive=y` option
- Checks if `pylint`'s output includes linting of `ignored.py`, which should not happen
- Cleans up by removing the temporary project directory after execution

Before using it, ensure that `pylint` is properly installed in your environment. You can install `pylint` using pip if it's not already installed:

```sh
pip install pylint
```

Please adjust any paths or commands as necessary to fit your specific operating system and environment configurations.