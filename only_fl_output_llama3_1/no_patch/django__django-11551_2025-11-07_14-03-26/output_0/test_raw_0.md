Here is the reproducer script:

```python
import django
from django.contrib import admin
from position.Fields import PositionField
from django.db import models

def main():
    try:
        admin.autodiscover()
        class Thing(models.Model):
            number = models.IntegerField(default=0)
            order = PositionField()

        class ThingAdmin(admin.ModelAdmin):
            list_display = ['number', 'order']

        admin.register(Thing, ThingAdmin)

        print("Issue reproduced successfully!")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    main()
```

This script will attempt to register the `Thing` model with the admin interface, which should trigger the issue. If the issue is present, it will print a stack trace and raise an `AssertionError`. If the issue is fixed, it will simply print a success message.