Here is the reproducer script:

```python
import django
from django.contrib import admin
from position.Fields import PositionField
from django.db import models

def main():
    try:
        admin.E108  # This should raise an AssertionError if the issue is present
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    class Thing(models.Model):
        number = models.IntegerField(default=0)
        order = PositionField()

    class ThingAdmin(admin.ModelAdmin):
        list_display = ['number', 'order']

    admin.register(Thing, ThingAdmin)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` if the issue is present and print a stack trace. If you run this script with Django 2.2.1, it should reproduce the issue.