Creating a reproducible script as you've outlined involves mocking or simulating the Django admin environment, which isn't straightforward due to its complex nature and reliance on a running Django project. This script assumes a Django project setup and will attempt to simulate form submission to the admin interface for a model with an inline form that does not properly handle default ArrayField values upon failed validation.

**Note:** This script won't work as standalone without a Django project context. It is meant to be placed in the root of a Django project where the models and admin registration described in your issue exist.

```python
# reproducer.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.test import Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings

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

def test_inline_form_default_issue():
    # Ensure a user exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass')
    
    client = Client()
    client.login(username='admin', password='pass')

    # Simulate the form submission process
    try:
        # First submission (expected to fail)
        response = client.post('/admin/my_app/thing/add/', {
            'relatedmodel_set-TOTAL_FORMS': '1',
            'relatedmodel_set-INITIAL_FORMS': '0',
            'relatedmodel_set-MIN_NUM_FORMS': '0',
            'relatedmodel_set-MAX_NUM_FORMS': '1000',
            'relatedmodel_set-0-plop': '["test"]',  # Input that should trigger validation failure
        }, follow=True)
        assert 'errors' in response.context, "Validation did not fail as expected."

        # Second submission (should also fail but doesn't)
        response = client.post('/admin/my_app/thing/add/', {
            'relatedmodel_set-TOTAL_FORMS': '1',
            'relatedmodel_set-INITIAL_FORMS': '0',
            'relatedmodel_set-MIN_NUM_FORMS': '0',
            'relatedmodel_set-MAX_NUM_FORMS': '1000',
            # No change to plop, simulating a user resubmitting without modification
        }, follow=True)
        assert 'errors' in response.context, "Validation erroneously passed on second submission."

        print("Issue reproduction failed: The issue seems to be fixed.")
    except AssertionError as ae:
        print("Issue is present.")
        print_stacktrace(ae)
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)

if __name__ == "__main__":
    test_inline_form_default_issue()
```

**Explanation:**
- This script sets up the Django environment and tries to simulate a user submitting a form with an inline formset through the Django admin site, specifically targeting the behavior you described.
- It attempts to login as a superuser and submit a form with a `ValidationError` expected on the first submission and checks if the invalid form data persists or not on a subsequent submission without changes, which simulates the described buggy behavior.
- The use of `assert` statements is to enforce the condition that the error must occur on the first submission and should persist on a second submission, reflecting the presence of the issue.

**Important Considerations:**
- The script assumes the existence of a Django project (`your_project.settings` needs to be replaced with the actual Django settings module).
- The targeted URL and form data must match the actual admin form structure and field names; adjustments are likely necessary to fit the specifics of your models and admin configuration.
- The mechanism to create a superuser programmatically assumes that it's being run in a development environment. This might need adjustments based on your actual user authentication setup.