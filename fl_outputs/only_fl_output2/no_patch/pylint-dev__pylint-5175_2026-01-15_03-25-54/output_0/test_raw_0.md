```python
# reproducer.py
import pylint.lint
import tempfile
import os
import sys

def check_pylint_issue():
    """
    This function creates a temporary Python file with the specified content
    that includes a function with *args documented, then runs pylint on this
    file to see if the described issue is reproduced.
    """

    code = '''
def function(file, *args, sep=";"):
    """Description of the function

    Parameters
    ----------
    file : str
        Path to the input.
    *args
        Relevant parameters.
    sep : str, optional
        File separator.
    """
    pass
'''

    # Write the code to a temporary file
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as temp:
        temp_name = temp.name
        temp.write(code)

    # Running pylint on the temporary file
    pylint_opts = [temp_name]
    linter = pylint.lint.Run(pylint_opts, do_exit=False)
    os.unlink(temp_name)  # Clean up temporary file

    # Checking for the specific pylint message id in the report
    for message in linter.linter.reporter.messages:
        if message.msg_id == "W9015":
            return f"Found issue with msg_id: {message.msg_id}"

    return None


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


def main():
    try:
        issue = check_pylint_issue()
        if issue:
            print(f"Issue detected: {issue}")
            raise AssertionError("Pylint failed to pass a documented *args without warning.")
        else:
            print("No issue detected. Pylint behavior as expected.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error if there's an exception
    else:
        sys.exit(0)  # Exit without error if issue is not detected

if __name__ == "__main__":
    main()
``` 

This script aims to reproduce the issue by creating a temporary Python script containing a function with `*args` and then running `pylint` on this script to check for the specific warning (`W9015`). It uses a simple exception handling mechanism to capture any errors, print a detailed stack trace if an error occurs, and manage script exit codes according to the outcome (successful check or error).