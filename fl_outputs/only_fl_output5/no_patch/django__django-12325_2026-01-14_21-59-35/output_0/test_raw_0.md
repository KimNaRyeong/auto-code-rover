```python
# reproducer.py
import sys
import os

def setup_django_env():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()

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
    setup_django_env()

    from django.db import models

    try:
        class Document(models.Model):
            pass

        class Picking(Document):
            # Intentionally placing `document_ptr` after `origin` to trigger the issue.
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')

        # If the model is successfully created without issues, the problem is resolved.
        print("Model creation successful. Issue appears to be resolved.")
        sys.exit(0)

    except Exception as e:
        print_stacktrace(e)
        # If an exception is caught, it means there's an issue with the model creation.
        assert "parent_link=True" in str(e), "Unexpected error message."
        # Exiting with non-zero if the exception is exactly as expected, to indicate issue presence.
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script is designed to check for a specific issue in Django model inheritance when multiple `OneToOneField` relations exist, and the `parent_link=True` attribute's behavior changes unexpectedly based on field order. By attempting to declare a model with a `OneToOneField` marked as a `parent_link`, following another `OneToOneField` not marked as such, we expect to trigger an `ImproperlyConfigured` exception that suggests adding `parent_link=True` to the non-parent link field, if the issue exists.

**Please Note:**
1. This script assumes that you have a Django project setup with the settings module located at `config.settings`. You may need to change the `'DJANGO_SETTINGS_MODULE', 'config.settings'` part to point to your actual Django settings module path.
2. Make sure to have Django installed in your environment where you run this script. You can install Django via pip if you haven't done so: `pip install django`.
3. This script uses the `assert` statement to specifically check for the presence of the issue based on the caught exception message. If the message or the nature of the issue changes, the assertion condition and the exception handling may need to be updated accordingly.
4. Adjustment to the script might be necessary if your Django project's setup varies from standard configurations, including how the Django environment is setup within the script.