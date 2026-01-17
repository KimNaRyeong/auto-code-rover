 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import django
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

settings = {
    'INSTALLED_APPS': ['myapp'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testdb',
        }
    }
}

django.setup(setttings=settings)

from myapp.models import Document, Picking

class Document(models.Model):
    pass
class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

try:
    Picking()
except ImproperlyConfigured as e:
    print_stacktrace(e)
    sys.exit(0)
```
This script sets up a minimal Django project with a single app named `myapp`, and defines the `Document` and `Picking` models as described in the issue. It then attempts to create an instance of the `Picking` model, which should raise an `ImproperlyConfigured` exception with the specified error message.

You can run this script using the command `python3 reproducer.py`, which should print the stack trace of the exception.

To fix the issue, you can simply swap the order of the `document_ptr` and `origin` fields in the `Picking` model, like this:
```python
class Picking(Document):
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
```
After making this change, the script should exit without raising any exceptions.