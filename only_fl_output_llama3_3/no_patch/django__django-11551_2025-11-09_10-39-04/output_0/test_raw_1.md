Here is the reproducer script:

```python
import django
from django.db import models
from position.Fields import PositionField

def main():
    try:
        admin.E108  # This should raise an AssertionError if the issue is present
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    class Thing(models.Model):
        number = models.IntegerField(default=0)
        order = PositionField()

    from django.contrib import admin
    from .models import Thing

    @admin.register(Thing)
    class ThingAdmin(admin.ModelAdmin):
        list_display = ['number', 'order']

if __name__ == "__main__":
    main()
```

This script should reproduce the issue by raising an `AssertionError` when running with Django 2.2.1 and print a stack trace.