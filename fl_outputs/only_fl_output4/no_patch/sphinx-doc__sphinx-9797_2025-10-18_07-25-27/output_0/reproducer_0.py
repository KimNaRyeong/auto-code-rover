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

class Parent:
    @classmethod
    def method(cls) -> int:
        """Return an integer."""
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42

try:
    parent_doc = Parent.method.__doc__
    child_doc = Child.method.__doc__
    # Verify inheritance of documentation
    assert child_doc == parent_doc, "Child method did not inherit parent documentation."
    print("Success: Documentation was inherited correctly.")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with a non-zero code to indicate issue presence
