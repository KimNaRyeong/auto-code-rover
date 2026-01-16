Given the specific requirements and ensuring the script works as expected, below is a Python script named `reproducer.py` designed to simulate the original issue with `pylint`'s `--recursive` option seemingly ignoring the `ignore-paths` setting. If the issue is reproduced successfully, it triggers an `AssertionError`. Please note, this script requires a slight adjustment in approach due to the complexity of mimicking `pylint` behavior strictly within a script.

The script will create a temporary Python project structure, including a `pyproject.toml` with `ignore-paths` configured. It will then programmatically invoke `pylint` on this structure and check the output to verify if files meant to be ignored were indeed skipped. If those files aren't ignored (i.e., `pylint` reports issues from within the ignored paths), it raises an `AssertionError`.

```python
import subprocess
import tempfile
import os

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

def run_pylint_with_ignore_paths():
    with tempfile.TemporaryDirectory() as tempdir:
        src_dir = os.path.join(tempdir, "src")
        gen_dir = os.path.join(src_dir, "gen")
        
        os.makedirs(gen_dir)
        
        # Create a Python file inside the 'gen' directory which should be ignored based on pyproject.toml settings
        with open(os.path.join(gen_dir, "should_ignore.py"), "w") as file:
            file.write("import os\n")
        
        # Create a pyproject.toml file with 'ignore-paths' configured
        with open(os.path.join(tempdir, "pyproject.toml"), "w") as file:
            file.write(
                "[tool.pylint.MASTER]\n"
                "ignore-paths = [\n"
                "  \"^src/gen/.*$\",\n"
                "]\n"
            )

        # Running pylint programmatically to ensure the current environment's pylint is used
        result = subprocess.run(
            ["pylint", "--recursive=y", src_dir],
            cwd=tempdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if the file that should be ignored is mentioned in pylint's output
        if "should_ignore.py" in result.stdout:
            raise AssertionError("pylint did not ignore the paths specified in pyproject.toml")

try:
    run_pylint_with_ignore_paths()
    print("The issue is not reproduced, pylint correctly ignored the specified paths.")
except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print("An unexpected error occurred.")
    print_stacktrace(e)
    raise
```

This script does not directly validate the `pylint` version or its configuration parsing, which means the specific details about why files in `ignore-paths` are not being ignored (if such an issue indeed exists in the provided `pylint` version) would still need direct observation from `pylint` outputs or deeper investigation into `pylint`'s behavior. Additionally, ensure that `pylint` is installed in your environment where this script is executed.