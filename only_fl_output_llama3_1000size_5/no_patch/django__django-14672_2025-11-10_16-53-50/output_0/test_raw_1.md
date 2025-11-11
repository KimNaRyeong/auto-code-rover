Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.apps import apps
from django.core.management import execute_from_command_line

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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broken_m2m_project.settings')
    try:
        from django.db.models import ManyToManyRel
        class Parent(models.Model):
            name = models.CharField(max_length=256)
        
        class ProxyParent(Parent):
            class Meta:
                proxy = True
        
        class Child(models.Model):
            parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
            many_to_many_field = models.ManyToManyField(
                to=Parent,
                through="ManyToManyModel",
                through_fields=['child', 'parent'],
                related_name="something"
            )
        
        class ManyToManyModel(models.Model):
            parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='+')
            child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='+')
            second_child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, default=None)
    except TypeError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

This script will raise a `TypeError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

Please note that you need to have Django installed in your Python environment for this script to work.