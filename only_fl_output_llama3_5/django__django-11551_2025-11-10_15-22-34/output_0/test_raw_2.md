I apologize for the mistake. Here is a new reproducer script that should reproduce the issue:

```python
import django
from position.Fields import PositionField
from django.db import models
from django.contrib import admin

def main():
    try:
        from django.contrib.admin.checks import _check_list_display
        ThingAdmin(Thing())
        _check_list_display()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    class Thing(models.Model):
        number = models.IntegerField(default=0)
        order = PositionField()

    class ThingAdmin(admin.ModelAdmin):
        list_display = ['number', 'order']

if __name__ == "__main__":
    main()
```

This script should be placed in a file named `reproducer.py` and run using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError`, print the stack trace, and exit with code 1.