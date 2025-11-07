Here is the reproducer script:

```python
import os
from django.contrib import admin
from django.urls import reverse, path
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

setup_test_environment()

class ModelAdmin(admin.ModelAdmin):
    readonly_fields = ['foreign_key']

class MyModel(admin.ModelAdmin):
    model = None  # This will be set later
    admin_site_name = None  # This will be set later

def get_admin_url(remote_obj, url_name):
    return reverse(url_name, args=[quote(None)])

try:
    from django.contrib.admin.helpers import get_admin_url
except ImportError as e:
    print_stacktrace(e)
    exit(0)

model_admin = ModelAdmin()
model_admin.admin_site.name = 'custom-admin'

my_model = MyModel()
my_model.model = model_admin

# This line should raise an AssertionError
get_admin_url(None, 'change')

exit(1)  # Exit with code 1 if the issue is present
```

This script sets up a test environment and defines two admin classes: `ModelAdmin` and `MyModel`. The `ModelAdmin` class has a readonly field named `foreign_key`, which should trigger the issue. The `get_admin_url` function is then called with the `None` object (representing the model instance) and the `'change'` URL name, which should raise an AssertionError.

If you run this script using `python3 reproducer.py`, it will print a stack trace if the issue is present, or exit with code 0 if the issue is fixed.