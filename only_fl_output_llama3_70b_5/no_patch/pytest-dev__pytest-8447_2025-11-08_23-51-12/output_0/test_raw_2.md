I apologize for the previous mistake. Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
import sys

def test_issue():
    try:
        # Simulate the pytest environment
        import pytest
        from _pytest.nodes import Item
        from pytest_black import BlackItem
        from pytest_checkdocs import CheckdocsItem

        # Create an instance of Item to simulate the parent
        parent = Item("parent")

        # Try to create instances of BlackItem and CheckdocsItem with unexpected keyword arguments
        BlackItem.from_parent(parent, fspath="path", path="path")
        CheckdocsItem.from_parent(parent, fspath="path", path="path")  # This should raise a TypeError

    except TypeError as e:
        if "got an unexpected keyword argument 'path'" in str(e):
            print_stacktrace(e)
            assert False, "Issue reproduced"
        else:
            print("Unexpected error:", file=sys.stderr)
            print_stacktrace(e)
            sys.exit(1)
    else:
        print("Issue fixed")
        sys.exit(0)

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

if __name__ == "__main__":
    test_issue()
```
This script will exit with code 1 if the issue is reproduced and code 0 if the issue is fixed.