Here is the reproducer script:

```python
import django
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.db import models

def main():
    try:
        # Create a model with verbose name
        class Article(models.Model):
            pub_date = models.DateTimeField("date published")

        # Create an admin user
        user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

        # Create an article instance
        article = Article(pub_date='2022-01-01')
        article.save()

        # Update the publication date
        article.pub_date = '2023-02-02'
        article.save()

        # Get the history of the model
        histories = LogEntry.objects.filter(object_id=article.pk, object_name='Article').order_by('-action_time')

        # Check if the history contains verbose names
        for history in histories:
            if not history.change_message.startswith('Changed date published.'):
                raise AssertionError("History does not contain verbose names")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

    else:
        print("Issue reproduced successfully")
        exit(0)


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


def setup_django():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbed.settings')
    from django.conf import settings


setup_django()
if __name__ == "__main__":
    main()

```

This script sets the DJANGO_SETTINGS_MODULE environment variable before running the test.