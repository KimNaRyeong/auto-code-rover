Here is the reproducer script:

```python
import django
from django.db import models
from position.Fields import PositionField

def main():
    try:
        ThingAdmin()
    except admin.E108 as e:
        print_stacktrace(e)
        exit(1)

    class Thing(models.Model):
        number = models.IntegerField(default=0)
        order = PositionField()

    from django.contrib import admin
    from .models import Thing

    class ThingAdmin(admin.ModelAdmin):
        list_display = ['number', 'order']

if __name__ == "__main__":
    main()
```

This script should reproduce the issue by raising an `admin.E108` exception when running with Django 2.2.1 and print a stack trace.