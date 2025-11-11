Here is the reproducer script:

```python
import django
from django.db import models

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
    from django.test import TestCase
    class Parent(models.Model):
        children = models.ManyToManyField('self')

    class Child(models.Model):
        parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    class TestDelete(TestCase):
        def test_delete(self):
            p1 = Parent.objects.create()
            c1 = Child(parent=p1)
            c2 = Child(parent=p1)

            p1.children.add(c1)
            p1.children.add(c2)

            c1.parent.delete(keep_parents=True)
            assert c2.parent is not None, "Parent of child should be preserved"

    if __name__ == "__main__":
        try:
            main()
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)
        else:
            exit(0)

if __name__ == "__main__":
    import sys
    from django.test.utils import setup_test_environment

    setup_test_environment()

    if sys.version_info < (3, 7):
        raise Exception("This reproducer requires Python 3.7 or higher.")

    main()
```

Please note that you need to have Django installed in your Python environment for this script to work.