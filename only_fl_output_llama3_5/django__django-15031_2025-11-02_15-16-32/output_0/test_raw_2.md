Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    return value.replace(',', ' ')

try:
    from django.utils.encoding import smart_str
    prepare_lookup_value('johnny,viola,gordon')
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("Issue not present")
```

This script tries to call the `prepare_lookup_value` function with a comma-separated string. If the issue is present, it will catch any exception that is raised, print the stack trace, and then exit with code 1.