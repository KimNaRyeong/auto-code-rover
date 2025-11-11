Here is the reproducer script:

```python
import django
from django.forms import DurationField
from django.utils.dateparse import parse_duration

def main():
    try:
        duration_field = DurationField()
        duration_field.clean('P3(3D')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up the Django environment and then attempts to clean a broken duration string using the `DurationField`. If an exception is raised, it prints the stack trace and raises an assertion error.