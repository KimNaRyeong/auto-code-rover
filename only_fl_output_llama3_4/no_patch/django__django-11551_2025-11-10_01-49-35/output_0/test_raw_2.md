Here is the reproducer script:

```python
import django
from django.db import models
from position.Fields import PositionField

def main():
    try:
        admin.E108
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

This script should be executed by `python3 reproducer.py`. If the issue is present, it will raise an AssertionError and print a stack trace.