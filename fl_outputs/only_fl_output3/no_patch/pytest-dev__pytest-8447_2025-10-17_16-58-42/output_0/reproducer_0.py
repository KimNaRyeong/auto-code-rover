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

def simulate_issue():
    class PluginItem:
        @classmethod
        def from_parent(cls, parent, **kw):
            # Mimic the node initialization logic that leads to the issue
            cls.validate_keywords(**kw)
            return cls()

        @staticmethod
        def validate_keywords(**kw):
            if 'path' in kw:
                raise TypeError("__init__() got an unexpected keyword argument 'path'")

    # Simulate plugins' behavior that leads to the TypeError exception
    try:
        PluginItem.from_parent(parent=None, path='/path/to/test_file.py')
        # If the issue is fixed, this line gets executed.
        return "Fixed"
    except TypeError as e:
        print_stacktrace(e)
        return "Present"

if __name__ == "__main__":
    issue_status = simulate_issue()
    assert issue_status == "Fixed", "The issue with unexpected keyword argument 'path' is still present."
    print("The issue appears to be fixed. Exiting with code 0.")
    sys.exit(0)
