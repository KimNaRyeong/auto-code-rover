To create a script that fulfills your requirements, it must execute pylint against a specific Python file that contains the function with the mentioned docstring issue. This script `reproducer.py` will run pylint programmatically against a simple Python script that includes the problematic function definition. The script checks pylint's output for the specific warning code (`W9015`) related to the documentation of `*args`. If the warning is present, it raises an `AssertionError`; if not, it exits gracefully with code `0`.

Firstly, here's the content for `reproducer.py`:

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

def check_pylint_output():
    # The problematic function is written to a temporary .py file for pylint to check
    function_code = """
def function(file, *args, sep=";"):
    \"\"\"Description of the function

    Parameters
    ----------
    file : str
        Path to the input.
    *args
        Relevant parameters.
    sep : str, optional
        File separator.
    \"\"\"
    pass
"""

    filename = "temp_function.py"
    with open(filename, "w") as f:
        f.write(function_code)

    try:
        # Running pylint on the created file
        result = subprocess.run(['pylint', filename], capture_output=True, text=True, check=True)

        # Looking for specific warning code in pylint output
        if "W9015" in result.stdout:
            raise AssertionError("W9015 warning detected for *args documentation")

    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code if pylint execution failed

    finally:
        # Clean up by removing the temporary file
        import os
        os.remove(filename)

    print("No issues detected, pylint passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    try:
        check_pylint_output()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code if the warning W9015 is detected
```

This script writes a temporary Python file with the function that should trigger the pylint warning, runs pylint on that file, checks the output for the warning code `W9015`, and manages errors and exceptions accordingly. If the pylint check passes without raising the specific warning, it means the issue is considered fixed, and the script exits with code `0`.

Please note that you need to have `pylint` installed in your environment for this script to work. You can install it via pip if you haven't already:

```sh
pip install pylint
```

Remember, this script assumes that pylint's behaviour and warning codes are consistent with the version you reported (`pylint 2.5.3`). Warning codes and pylint's internal behavior may change in future versions.