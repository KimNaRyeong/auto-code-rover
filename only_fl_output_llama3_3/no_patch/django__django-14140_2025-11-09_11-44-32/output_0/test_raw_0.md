Here is the `reproducer.py` file that reproduces the issue:

```python
import django
from django.db.models import Q, Exists
from django.contrib.auth import get_user_model

def main():
    try:
        Q(Exists(get_user_model().objects.filter(username='jim'))).deconstruct()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception not raised")

if __name__ == "__main__":
    main()
```

You can run this file by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and raise an `AssertionError`.