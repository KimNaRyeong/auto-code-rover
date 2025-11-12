Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.apps import apps

def make_hashable(obj):
    return tuple(sorted((k, v) for k, v in asdict(obj).items()))

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

def asdict(obj):
    return {k: v for k, v in obj.__dict__.items()}

def main():
    try:
        apps.populate([models.ModuleLoader('app', os.path.join(os.getcwd(), 'app'))])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will attempt to create the models and populate the app. If an error occurs, it will print the stack trace and exit with code 1.