import os
import sys

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

def test_issue():
    try:
        # Reproduce the issue by running pytest with plugins
        os.system("pip install -q pytest-black pytest-checkdocs")
        os.system("pytest --black --checkdocs test_something.py")
        assert False, "Expected TypeError: __init__() got an unexpected keyword argument 'path'"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    if not os.path.exists('test_something.py'):
        with open('test_something.py', 'w') as f:
            pass
    test_issue()
