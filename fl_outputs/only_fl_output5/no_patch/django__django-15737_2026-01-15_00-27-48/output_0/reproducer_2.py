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
    def __init__(self, name):
        self.name = name
        self.id = None

    def save(self):
        # Simulate saving to the database and getting an ID
        self.id = 1

class Child:
    def __init__(self, parent):
        self.parent = parent
        self.parent_id = None

    def save(self):
        if self.parent.id is not None:
            self.parent_id = self.parent.id
        # This line simulates the issue where the original parent reference is cleared
        # when only the parent_id should be updated.
        self.parent = None

try:
    parent = Parent(name='Parent')
    child = Child(parent=parent)
    parent.save()  # This should assign an ID to parent, mimicking a database save
    child.save()  # Attempt to save child, which should simulate setting the parent_id and clearing parent
    
    assert child.parent is not None, "Child's parent reference was unexpectedly cleared."
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # To indicate failure due to the assertion error
else:
    print("The issue has been fixed.")
    exit(0)
