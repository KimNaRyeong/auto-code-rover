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
    Execute the given shell command and return its output, errors.
    This is adjusted to be compatible with Python 3.6 by avoiding capture_output parameter.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    return stdout, stderr

def check_issue():
    cmd = 'python -m django shell -c "import django\ndef f():\n    print(django.__version__)\nf()"'
    
    stdout, stderr = run_shell_command(cmd)

    # Checking if the command results in a NameError for 'django'
    if 'NameError: name \'django\'' in stderr:
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
