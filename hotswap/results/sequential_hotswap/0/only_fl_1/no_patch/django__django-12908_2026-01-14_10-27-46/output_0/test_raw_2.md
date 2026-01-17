To directly address your request, let's structure `reproducer.py` assuming you have a Django environment set up for this script to run. This includes a Django project with a model named `Sample` and at least a user model for authentication purposes. Remember, this script will require an actual Django environment to execute, which involves having Django installed, a project created, an app created, and the `Sample` model defined within that app. Also, ensure Django is properly configured to connect to a database where these models exist.

Here's how you can structure `reproducer.py`:

```python
import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.db.models import Value, IntegerField
from django.contrib.auth import get_user_model
from your_app.models import Sample  # Adjust 'your_app' to the actual app name where Sample model is defined

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

def get_or_create_admin_user():
    User = get_user_model()
    user, created = User.objects.get_or_create(username='admin')  # Simple example, adjust as necessary
    return user

def main():
    user = get_or_create_admin_user()
    # Preparing data
    Sample.objects.create(user=user, name="Sam1")
    Sample.objects.create(user=user, name="Sam2 acid")
    Sample.objects.create(user=user, name="Sam3")
    Sample.objects.create(user=user, name="Sam4 acid")
    Sample.objects.create(user=user, name="Dub")
    Sample.objects.create(user=user, name="Dub")
    Sample.objects.create(user=user, name="Dub")
    
    # Attempt to reproduce the issue
    try:
        qs = Sample.objects.filter(user=user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs_union = qs1.union(qs2)
        qs_distinct = qs_union.order_by('name').distinct('name')  # This is the main focus
        
        if qs_distinct.count() != 2:
            raise AssertionError("Distinct after union did not produce the expected result")

        print("The issue could not be reproduced, distinct() after union() worked as expected.")

    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```

**Note**: 
- Replace `'your_project.settings'` with the path to your actual Django project settings.
- Adjust the model and user creation logic as per your actual models and project setup. This script assumes `Sample` model has at least `user` (ForeignKey to User model) and `name` (CharField) fields.
- The Django execution environment must be initialized with `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')` and `django.setup()` for standalone scripts to work. Adjust `'your_project.settings'` to point to the correct settings module of your Django project.
- This example script assumes a very simple user setup for authentication, which might not match your project's actual authentication setup. Adjust accordingly.
- The effectiveness of reproducing the issue heavily relies on the accuracy of the `Sample` model and data assumptions matching your actual environment.