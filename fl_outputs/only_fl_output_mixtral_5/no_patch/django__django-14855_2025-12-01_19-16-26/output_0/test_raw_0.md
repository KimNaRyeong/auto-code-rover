 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import admin
from django.urls import reverse
from django.test import RequestFactory, SimpleTestCase

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

class TestAdminSite(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = admin.CustomAdminSite()
        self.model_admin = MyModelAdmin(model=MyModel, admin_site=self.site)
        self.model_admin.admin_site.register(MyModel)

    def test_get_admin_url_with_readonly_field(self):
        remote_obj = MyModel()
        request = self.factory.get('/admin/myapp/mymodel/1/')
        url = reverse(
            'admin:myapp_mymodel_change',
            args=[quote(remote_obj.pk)],
            current_app=self.model_admin.admin_site.name
        )
        self.assertEqual(url, '/custom-admin/myapp/mymodel/1/')

        # Uncomment the following line to reproduce the issue
        # url = reverse('admin:myapp_mymodel_change', args=[quote(remote_obj.pk)])

        with self.assertRaises(AssertionError):
            self.assertEqual(url, '/admin/myapp/mymodel/1/')

if __name__ == '__main__':
    try:
        TestAdminSite().test_get_admin_url_with_readonly_field()
    except Exception as e:
        print_stacktrace(e)
        raise
```
The `MyModelAdmin` class is a custom admin class that has a `readonly_fields` attribute set to `('related_object',)`. The `MyModel` class is a simple model class that has a `name` attribute and a `related_object` attribute.

The `TestAdminSite` class is a test case that sets up a custom admin site, registers the `MyModel` class with the admin site, and defines a test method `test_get_admin_url_with_readonly_field()`.

In the test method, a `RequestFactory` is used to create a GET request to the admin URL `/admin/myapp/mymodel/1/`. The `reverse()` function is then called to generate the URL for the change page of the `MyModel` class with the primary key of the `remote_obj` instance.

If the `current_app` parameter is passed to the `reverse()` function, the generated URL will be `/custom-admin/myapp/mymodel/1/`, which is the expected URL for the custom admin site. However, if the `current_app` parameter is not passed, the generated URL will be `/admin/myapp/mymodel/1/`, which is the default admin URL.

To reproduce the issue, simply uncomment the line that calls `reverse()` without the `current_app` parameter. This will cause the test to fail with an `AssertionError`, and the stack trace will be printed to the console.

If the issue is fixed, the test should pass and the script should exit with code 0.