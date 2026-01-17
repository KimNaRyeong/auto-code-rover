To accurately reproduce the reported issue and verify its presence or absence, let’s perform an approach where we simulate the scenario within a Python script (`reproducer.py`) that programmatically checks for the duplication of logging messages when executed under conditions similar to those described. This script will execute a `pytest` test function that contains both the condition check and a logging operation within a test case. Post-execution, it will inspect the output to determine if the logging duplication issue occurs. If the issue persists, it will raise an `AssertionError` and print a detailed stack trace showing where the problem was detected. Conversely, if the issue is not present, the script will terminate with an exit code of 0, indicating the problem is fixed.

```python
import subprocess
import re
import tempfile
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

def test_for_issue():
    # Create a temporary test file
    test_script_content = """import logging
import pytest

def _check_cond():
    logging.warning("_check_cond")
    return True

@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")
    assert False
"""
    with tempfile.NamedTemporaryFile("w+", suffix=".py") as temp_py_file:
        temp_py_file.write(test_script_content)
        temp_py_file.flush()

        # Execute the pytest with the generated test script
        result = subprocess.run(['pytest', temp_py_file.name], capture_output=True, text=True)

        # Check if the logging message is duplicated in standard error output
        if "Schmift" in result.stderr and "Captured log call" in result.stdout:
            # Issue reproduced
            return True, result.stderr + "\n" + result.stdout
        else:
            # Issue not reproduced
            return False, result.stderr + "\n" + result.stdout

def main():
    issue_detected, output = test_for_issue()
    try:
        if issue_detected:
            raise AssertionError("The duplicate logging issue was encountered.")
        else:
            print("No duplication in stderr detected: Issue appears to be fixed.")
            sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        print("\n\nAdditional Output For Diagnosis:\n", output)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Steps to Use:
1. Save the above script to a file named `reproducer.py` in the root directory of your project.
2. Ensure you have `pytest` installed in your environment. If you don't, install it using `pip install pytest`.
3. Run the script using Python 3: `python3 reproducer.py`.

This script works by creating a temporary Python file that mimics the scenario outlined in the issue description, then running `pytest` on this file. It captures and analyzes the command's output to check for the reported undesired behavior. If the logging output "Schmift" appears in stderr while also being properly captured as per pytest's logging mechanism (indicating a duplication of the log message), the script confirms that the issue is present. When the issue is detected, the script prints a detailed stack trace using the provided `print_stacktrace` function and additional output for diagnosis before exiting with an error code, thus satisfying the requirements to raise an `AssertionError`, print a detailed stack trace, and exit accordingly based on the presence of the issue.