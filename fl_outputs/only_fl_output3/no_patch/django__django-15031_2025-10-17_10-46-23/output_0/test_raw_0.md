Below is a script named `reproducer.py` designed to reproduce the described Django admin issue related to filtering with values that contain commas.

Please ensure you have a Django project set up with the `User` model available from `django.contrib.auth.models` for this script to work as expected. The script should be run within the environment where your Django project dependencies are installed.

```python
import os
import django
from django.core.exceptions import FieldError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest

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

def setup_test_environment():
    User.objects.bulk_create([
        User(username='john,doe'),
        User(username='jane,roe'),
        User(username='johnny'),
        User(username='viola')
    ])

def reproduce_comma_issue():
    setup_test_environment()
    
    request = HttpRequest()
    request.GET = {'username__in': 'john,doe,jane,roe'}
    
    model_admin = ModelAdmin(User, AdminSite())
    changelist = ChangeList(
        request, 
        User, 
        model_admin.list_display, 
        model_admin.list_display_links, 
        model_admin.list_filter, 
        model_admin.date_hierarchy, 
        model_admin.search_fields, 
        model_admin.list_select_related, 
        model_admin.list_per_page, 
        model_admin.list_max_show_all, 
        model_admin.list_editable, 
        model_admin,
    )
    
    try:
        assert changelist.get_queryset(request).count() == 2, "Issue reproduced: Cannot filter with comma-containing values"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == '__main__':
    django.setup()
    try:
        reproduce_comma_issue()
    except Exception as e:
        print_stacktrace(e)
    else:
        print("Issue is not present or has been fixed.")
```

In the script:

- It first sets up the Django environment to use the settings of your project (`'your_project.settings'` needs to be replaced with the path to your actual settings module).
- It defines a function `setup_test_environment` to populate the `User` model with sample data. 
- The `reproduce_comma_issue` function simulates the Django admin list filtering with a query parameter that contains commas, aiming to trigger the assertion error when the issue exists as described.
- Remember to replace `'your_project.settings'` with the Python path to your actual Django settings module.
- The script requires that your Django project has the `User` model from `django.contrib.auth.models` and that you've set up your database accordingly.

This script will raise an `AssertionError` if it can't filter by username values containing commas, thus reproducing the issue.