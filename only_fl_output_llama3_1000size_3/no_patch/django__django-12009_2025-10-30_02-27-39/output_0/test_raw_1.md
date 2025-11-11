I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
import sys
from django.core import management
from pkg_resources import load_entry_point

def main():
    try:
        if __name__ == "__main__":
            entry_point = load_entry_point('Django==1.7', 'console_scripts', 'django-admin')
            entry_point()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == '__main__':
    sys.exit(main())
```

This script attempts to load the `django-admin` entry point using `pkg_resources.load_entry_point()` and then execute it. This should reproduce the issue of installing both `/usr/bin/django-admin` and `/usr/bin/django-admin.py`.