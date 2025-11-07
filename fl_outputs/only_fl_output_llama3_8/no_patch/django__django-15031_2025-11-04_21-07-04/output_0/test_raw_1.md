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
    django.setup()
    main()

```

This script sets up the Django environment before running the test.