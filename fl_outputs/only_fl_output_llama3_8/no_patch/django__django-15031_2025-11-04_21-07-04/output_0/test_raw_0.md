Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    value = str(value)  # convert to string
    if ',' in value:
        raise ValueError(f"Comma not allowed: {value}")
    return value

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',)

admin.site.register(User, CustomUserAdmin)

def main():
    try:
        User.objects.filter(username__in='johnny,viola,gordon')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script defines a custom admin model for the `User` model and attempts to filter users by username using the `username__in` lookup. If an exception is raised, it prints the stack trace and raises the same exception again.

You can run this script with `python3 reproducer.py` to reproduce the issue.