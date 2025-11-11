Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

def main():
    try:
        from django.contrib.admin.checks import _check_list_display
        _check_list_display(admin, ThingAdmin(Thing))
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