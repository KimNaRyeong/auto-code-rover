import sys
import subprocess
from django.core.management import execute_from_command_line

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

def main():
    command = """
import django
def f():
    print(django.__version__)
f()
"""
    try:
        subprocess.check_output(['python', '-m', 'django', 'shell', '-c', command])
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        assert False, "Issue is present"
    else:
        print("Issue is fixed")
        sys.exit(0)

if __name__ == '__main__':
    main()
