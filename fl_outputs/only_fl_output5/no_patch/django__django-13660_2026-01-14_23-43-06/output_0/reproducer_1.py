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

def run_shell_command(cmd: str):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result

def reproduce_issue():
    python_code = '''
import django
def f():
    print(django.__version__)
f()
'''
    cmd = '''python -m django shell -c "{}"'''.format(python_code.strip())
    result = run_shell_command(cmd)
    if "NameError: name 'django' is not defined" in result.stderr:
        return False, result.stderr
    else:
        return True, ''

def main():
    issue_fixed, stderr_output = reproduce_issue()
    if not issue_fixed:
        try:
            raise AssertionError("The issue is present")
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)  # Exit with a non-zero code to indicate failure
    else:
        print("Issue is fixed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
