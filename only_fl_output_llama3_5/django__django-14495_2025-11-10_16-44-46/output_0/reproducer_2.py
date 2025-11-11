import os
import sys
from django.core.management import execute_from_command_line

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
        os.chdir('testproj')
        execute_from_command_line(['manage.py', 'migrate', '--fake', 'testproj', '0001_initial'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected KeyError")

if __name__ == '__main__':
    main()
