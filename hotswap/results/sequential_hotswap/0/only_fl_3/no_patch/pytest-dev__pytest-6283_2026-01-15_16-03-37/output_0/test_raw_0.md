To address your request, I've created a Python script named `reproducer.py` that attempts to reproduce the issue described. This script will check if the logging call from a function used in a `@pytest.mark.skipif` decorator condition results in duplicated log messages in stderr when running tests. It will raise an `AssertionError` if the issue is present, thereby printing a stack trace. Conversely, it will exit with code 0 if the issue is correctly handled (i.e., if the log message "Schmift" is not duplicated in stderr).

```python
import logging
import subprocess
import tempfile
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

def run_test_script_with_logging_in_skipif():
    test_script_content = """
import logging
import pytest

def _check_cond():
    logging.warning("_check_cond")
    return True

@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")
    assert False
"""

    with tempfile.NamedTemporaryFile("w+", suffix=".py") as test_script:
        test_script.write(test_script_content)
        test_script.flush()
        
        result = subprocess.run(["pytest", test_script.name], capture_output=True, text=True)
        captured_stderr = result.stderr

        if "WARNING:root:Schmift" in captured_stderr:
            error_message = "Log message 'Schmift' is duplicated to stderr."
            raise AssertionError(error_message)
        else:
            print("No duplication in stderr. Issue seems fixed.")

try:
    run_test_script_with_logging_in_skipif()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
```

### Instructions:
1. Save the script to a file named `reproducer.py` in the root directory of your project.
2. Ensure you have pytest installed and accessible in your environment. If not, you can install it via `pip install pytest`.
3. Run the script using the command `python3 reproducer.py`.

- If the issue is present, the script will print a stack trace describing where the `AssertionError` was raised and then exit with code 1.
- If the issue is fixed (i.e., log messages are not being duplicated to stderr), the script will print "No duplication in stderr. Issue seems fixed." and exit with code 0.