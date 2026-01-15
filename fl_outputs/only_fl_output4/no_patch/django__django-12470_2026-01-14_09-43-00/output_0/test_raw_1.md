```python
# reproducer.py

import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line

        settings.configure(
            INSTALLED_APPS=["__main__"],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            USE_TZ=True,
        )

        import django
        django.setup()

        from django.db import models

        class Parent(models.Model):
            class Meta:
                ordering = ["-pk"]

        class Child(Parent):
            pass

        execute_from_command_line(['manage.py', 'migrate'])

        query = str(Child.objects.all().query)
        if 'DESC' not in query:
            raise AssertionError("The order in the generated query is not DESC as expected.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("The issue is fixed or not present.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the described issue in a standalone Django setup. It first configures Django settings necessary for running in-memory tests and defines two models `Parent` and `Child` in adherence to the issue description. It then programmatically applies migrations to create these models in an SQLite database. After setting up, the script queries the `Child` model, constructs the corresponding SQL query as a string, and checks if `'DESC'` (indicating descending order) is part of the query or not. If the check fails (meaning ASC order is used instead of DESC), an `AssertionError` is raised, and the script prints a stack trace of the issue. If no exception is raised, the script concludes the issue is not present or has been fixed, and exits with code 0.