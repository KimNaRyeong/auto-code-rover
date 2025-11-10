Here is the reproducer script:

```python
import django
from django.contrib import admin
from position.Fields import PositionField
from django.db import models

def main():
    try:
        from django.contrib.admin.checks import _check_list_display
        _check_list_display(admin, ThingAdmin)
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

This script should be run with Python 3. If the issue is present, it will raise an AssertionError and print a stack trace of the error.