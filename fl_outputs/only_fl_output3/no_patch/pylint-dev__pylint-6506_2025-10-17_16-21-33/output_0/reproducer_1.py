import sys
from pylint import epylint as lint

def reproduce_issue():
    try:
        # Instead of using subprocess, we use pylint's epylint interface
        (pylint_stdout, pylint_stderr) = lint.py_run('dummy.py -Q', return_std=True)
        
        # Capturing output from pylint
        stdout_content = pylint_stdout.getvalue()
        stderr_content = pylint_stderr.getvalue()

        # Verifying that no traceback is present in stderr_content
        assert "Traceback" not in stderr_content, "Traceback should not be present in the error for unrecognized options."
        assert "Unrecognized option found: Q" in stderr_content, "Expected error message not found."
        
        # Additional logic to ensure specific expected behavior could be added here
    
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

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

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    print("No issue detected. Pylint behaves as expected.")
    sys.exit(0)
