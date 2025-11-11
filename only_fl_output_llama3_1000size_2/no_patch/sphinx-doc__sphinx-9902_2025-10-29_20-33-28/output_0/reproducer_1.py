import sphinx
from sphinx.ext import autodoc
from sphinx.util import inspect
from functools import wraps

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

def test_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Failed to reproduce the issue")
    return wrapper

@test_issue
def test_issue():
    from my_library.module1 import mol
    if not isinstance(mol, dict) or 'type' not in mol or 'value' not in mol:
        raise Exception("mol is not a dictionary with keys 'type' and 'value'")

if __name__ == "__main__":
    test_issue()
