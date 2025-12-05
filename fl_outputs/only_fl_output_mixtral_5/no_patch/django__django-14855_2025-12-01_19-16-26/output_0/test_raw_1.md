 I apologize for the confusion. Here is an updated `reproducer.py` file that should reproduce the issue:
```python
import django
import admin
from django.urls import reverse
from django.test import RequestFactory, TestCase

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'related_object')
    readonly_fields = ('related_object',)

class MyModel(object):
    name = 'My Model'
    related_object = None

class CustomAdminSite(admin.AdminSite):
    name = 'custom-admin'

class TestAdminSite(TestCase):
    def setUp(self):
        django.setup()
        self.factory = RequestFactory()
        self.site = CustomAdminSite()
        self.model_admin = MyModelAdmin(model=MyModel, admin_site=self.site)
        self.model_admin.admin_site.register(MyModel)

    def test_get_admin_url_with_readonly_field(self):
        remote_obj = MyModel()
        request = self.factory.get('/admin/myapp/mymodel/1/')
        with self.assertRaises(AssertionError):
            url = reverse(
                'admin:myapp_mymodel_change',
                args=[remote_obj.pk]
            )
            self.assertEqual(url, '/custom-admin/myapp/mymodel/1/')

if __name__ == '__main__':
    try:
        TestAdminSite().test_get_admin_url_with_readonly_field()
    except Exception as e:
        print_stacktrace(e)
        raise
```
This script creates a custom admin site with the name `custom-admin`, and registers a model with a `readonly_fields` attribute set to `('related_object',)`.

The `test_get_admin_url_with_readonly_field()` method creates a GET request to the admin URL `/admin/myapp/mymodel/1/`, and then calls `reverse()` to generate the URL for the change page of the `MyModel` class with the primary key of the `remote_obj` instance.

Since the `current_app` parameter is not passed to the `reverse()` function, the generated URL will be `/admin/myapp/mymodel/1/`, which is the default admin URL. However, the expected URL is `/custom-admin/myapp/mymodel/1/`.

To reproduce the issue, simply run the script with `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace to the console.

If the issue is fixed, the script should exit with code 0.