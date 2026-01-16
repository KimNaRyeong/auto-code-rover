Given your requirements, this Python script will attempt to reproduce the issue within a Django environment, using models directly defined within it. Since `django.setup()` needs to be called after configuring settings but before defining models that require Django's model infrastructure, the structure slightly adjusts to ensure settings are appropriately configured before model declaration. Here's how you can construct `reproducer.py`:

```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import Q, FilteredRelation

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',  # Allows the script to find its own models for registration
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

django.setup()

# Model definitions must occur after django.setup()
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

# Now that the models are defined, we can demonstrate the issue.
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        Author.objects.create(name="Author 1")
        Book.objects.create(title="Poem by Alice", author_id=1)

        query = Author.objects.annotate(
            book_alice=FilteredRelation('books', condition=Q(books__title__iexact='poem by alice')),
        ).exclude(book_alice__isnull=False)

        list(query)  # Force the query to run

        print("The issue did not manifest.")
    except FieldError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code to indicate an issue was encountered

if __name__ == "__main__":
    reproduce_issue()
```

**Usage Instructions:**

- Ensure you have Django installed in your Python environment. If not, you can install it via pip: `pip install django`.
- Save this script as `reproducer.py` in the root directory of your Django project (or any other directory if you're executing it in isolation).
- Run the script using `python3 reproducer.py`.

The provided script configures Django to use an in-memory SQLite database for simplicity, making it self-contained and easy to run in any environment with Django installed. It's designed to directly reproduce the issue based on your description, and it will exit with an error code (1) if the issue is successfully reproduced.