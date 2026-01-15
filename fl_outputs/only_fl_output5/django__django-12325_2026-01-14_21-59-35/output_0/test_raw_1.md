Given the feedback, I'll simplify the previous approach to ensure the Django settings configuration issue doesn't prevent the script from running. We will use a standalone Django configuration within the script itself to avoid external dependencies.

Let's redo the `reproducer.py` with the minimal setup necessary to illustrate the issue without requiring a predefined Django project settings module.

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
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            '__main__',  # Register this module as an app
        ],
        SECRET_KEY='fake-key',
    )

    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'check'])

    from django.db import models

    try:
        class Document(models.Model):
            pass
        
        class Picking(Document):
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')

        # Trigger model system check
        from django.core.management import call_command
        call_command('makemigrations', '__main__')

        print("Model creation successful. Issue appears to be resolved.")
        sys.exit(0)

    except Exception as e:
        print_stacktrace(e)
        assert "Add parent_link=True to __main__.Picking.origin." in str(e), "Unexpected error message."
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Note:**

- This script integrates a minimal Django configuration directly, removing the need for an external settings module.
- It includes model definition inline to check against the reported issue.
- The configuration uses an in-memory SQLite database for simplicity, omitting persistent storage requirements.
- By calling `makemigrations` for the app '__main__', it leverages Django's system checks, which should highlight misconfigurations related to model inheritance and `OneToOneField`.
- If the Django ORM or migrations system behaves as expected (either by raising an expected exception or not), the script dutifully reports by exiting with code `0` (no issue found) or `1` (issue present), printing a relevant stack trace for diagnostics.

Ensure you have Django installed in your environment (`pip install Django`) when running this script.