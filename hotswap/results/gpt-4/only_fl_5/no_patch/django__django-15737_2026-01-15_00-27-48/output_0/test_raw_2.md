To correctly reproduce the described issue within a Python environment while considering it's related to Django ORM's handling of relationships and cached references, we will need to simulate a portion of Django's ORM behavior concerning foreign keys and model saving. Since actual Django ORM behavior is quite complex and tied to database interactions, the following script will primarily focus on illustrating the specific issue of the unnecessary clearing of cached references in a simplified context.

We'll create mock classes that mimic `Parent` and `Child` models with minimalistic save logic and caching mechanism to illustrate the problem. To detect the issue, the script will check if the cached reference to the `Parent` object is cleared after saving the `Child` object.

```python
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
```

This script aims to mimic the Django ORM behavior in relation to your issue, particularly focusing on the unnecessary clearing of the cached `Parent` object reference in the `Child` instance after saving. If executed in an environment where the issue is present (though hypothetically, since this script doesn't interact with Django directly), it will raise an `AssertionError` to indicate the unwanted behavior. When the issue is fixed – meaning that the cached reference to `Parent` is not cleared after `Child` is saved (you'd need to adjust the mocked `save` method to reflect this) – the script will exit with code 0, indicating the absence of the issue.