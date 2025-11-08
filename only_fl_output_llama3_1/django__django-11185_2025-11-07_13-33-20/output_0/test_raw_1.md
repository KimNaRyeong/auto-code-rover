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
    settings_module = 'django_project.settings'
    django.setup(settings_module)

    class ParentModel(models.Model):
        children = models.ManyToManyField('ChildModel')

    class ChildModel(models.Model):
        parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

    parent1 = ParentModel.objects.create()
    child1 = ChildModel(parent=parent1)
    child1.save()

    parent2 = ParentModel.objects.create()
    child2 = ChildModel(parent=parent2)
    child2.save()

    try:
        parent1.delete(keep_parents=True)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates a Django project and then attempts to reproduce the issue by deleting a model with `keep_parents=True`. If the issue is present, an `AssertionError` will be raised and caught by the script, which will print a stack trace.