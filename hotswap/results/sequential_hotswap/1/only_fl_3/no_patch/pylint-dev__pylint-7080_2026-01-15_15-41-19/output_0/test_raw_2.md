To create a standalone Python script named `reproducer.py` that reproduces the described issue with pylint's `--recursive=y` and `ignore-paths` settings, and adheres to the provided instructions, follow this implementation:

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

def run_pylint():
    try:
        # Clean previous pylint output if exists
        if os.path.exists("pylint_output.txt"):
            os.remove("pylint_output.txt")
        
        # Run pylint command as outlined in the issue
        result = subprocess.run(["pylint", "--recursive=y", "src/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Write output to a file for investigation
        with open("pylint_output.txt", "w") as file:
            file.write(result.stdout)

        # Check Pylint output for any ignored path issues
        if "src/gen/" in result.stdout:
            raise AssertionError("pylint's `ignore-paths` setting was ignored.")

        print("Pylint correctly ignored paths specified in `ignore-paths`.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code to indicate failure
    else:
        sys.exit(0)  # Exit with success code

if __name__ == "__main__":
    run_pylint()
```

Instructions for running `reproducer.py`:

1. Ensure `pylint` is installed in your environment:
    ```bash
    pip install pylint
    ```

2. Place `reproducer.py` at the root directory of your project.

3. Make sure you have the `src/` directory structure as described in your issue, including some files inside `src/gen/` that would typically trigger lint warnings or errors.

4. Ensure your `pyproject.toml` is configured with the `ignore-paths` setting as described in your issue.

5. Execute the script using Python:
    ```bash
    python3 reproducer.py
    ```

The script will check if `pylint` respects the `ignore-paths` configuration and excludes files in the specified paths from linting when run with the `--recursive=y` option. If the issue is reproduced, the script will raise an `AssertionError`, print the stack trace, and exit with code 1. If the issue is fixed or cannot be reproduced, it will simply exit with code 0.