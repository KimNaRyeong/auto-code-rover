Here is the reproducer script:

```python
import os
import django
from django.db import models

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
    django.setup()

    from myapp.models import Parent, Child

    class Meta:
        ordering = ["-pk"]

    try:
        print(Child.objects.all().query)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, defines the `Parent` and `Child` models, and then attempts to query the `Child` model. If an issue is present (i.e., the ordering is not descending), it prints the stack trace using the provided function and raises an assertion error.

To run this script, create a new directory for your project, navigate into it, and execute the script with Python 3: `python3 reproducer.py`.