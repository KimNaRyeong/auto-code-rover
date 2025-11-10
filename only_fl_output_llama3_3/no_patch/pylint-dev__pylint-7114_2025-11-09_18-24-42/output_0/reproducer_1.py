import os
import sys
from functools import lru_cache

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
        os.makedirs('a')
        with open('a/__init__.py', 'w') as f:
            pass
        with open('a/a.py', 'w') as f:
            pass
        with open('r.py', 'w') as f:
            f.write("from a import b\n")

        # Run pylint and check for error
        os.system("pylint a")
        if os.path.exists("a/__init__.py"):
            raise AssertionError("Linting failed")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    try:
        # Rename a.py to c.py
        os.rename('a/a.py', 'a/c.py')
        os.system("pylint a")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
