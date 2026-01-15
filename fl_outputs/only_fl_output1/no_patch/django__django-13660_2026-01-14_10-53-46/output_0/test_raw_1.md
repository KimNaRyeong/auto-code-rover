Given the information and requirements provided, let's adjust the script to address the issues previously encountered, including the compatibility with Python 3.6 where the `text` parameter should be replaced with `universal_newlines` for `subprocess.run` to ensure string handling of input and output. This updated script aims to reproduce the issue stated, raising an `AssertionError` when the issue is detected and exiting with code 0 when it's not.


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

def run_shell_command(command: str):
    """
    Execute the given shell command and return its output.
    Ensures compatibility with Python versions before 3.7 by using universal_newlines instead of text.
    """
    result = subprocess.run(command, shell=True, universal_newlines=True, capture_output=True)
    return result

def check_issue():
    # Command to execute Django shell
    cmd = """python -m django shell -c "import django\\ndef f():\\n    print(django.__version__)\\nf()" """
    
    result = run_shell_command(cmd)

    # Checking if the command results in a NameError for 'django'
    if 'NameError: name \'django\'' in result.stderr:
        print("Issue present. Printing Stack Trace...")
        try:
            raise Exception("Django context not loaded in shell with -c")
        except Exception as exc:
            print_stacktrace(exc)
            raise AssertionError("Issue reproduced successfully.")
    else:
        print("No issue detected. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    check_issue()
```

### Key Adjustments:

1. **Subprocess Compatibility**: The `universal_newlines=True` parameter is used instead of `text=True` for `subprocess.run` to maintain compatibility with Python 3.6 environments. This change ensures that inputs are from and outputs are returned as strings.

2. **Command Execution**: The `cmd` variable contains a command that attempts to execute Django shell with `-c` and run Python code that imports Django and accesses its version. This is the critical part designed to reproduce the issue described.

3. **Error Handling**: The script checks the output (especially `stderr`) for a `NameError` regarding the 'django' name, which signifies the problem is present. If found, it raises an `AssertionError`.

4. **Stack Trace Printing**: Upon catching the exception indicating the issue's presence, a detailed stack trace is printed using the `print_stacktrace` function.

Run this script in the root directory of a Django project configuration to test for the issue. Remember that the Django environment needs to be set up correctly for this script to run as intended.