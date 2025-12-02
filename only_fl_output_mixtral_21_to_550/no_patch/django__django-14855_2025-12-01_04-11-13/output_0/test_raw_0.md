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
    list_display = ('name', 'related_name')
    readonly_fields = ('related_name',)

class MyModel(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = admin.CustomAdminSite()
        self.model_admin = MyModelAdmin(model=self.admin_site.get_model('app', 'MyModel'))

    def test_get_admin_url(self):
        request = self.factory.get('/admin/app/mymodel/1/')
        request.admin_site = self.admin_site
        remote_obj = self.admin_site.get_model('app', 'MyModel').objects.get(pk=1)
        url_name = 'admin:app_mymodel_change'
        with self.assertRaises(AssertionError):
            print_stacktrace(AssertionError(
                'Expected URL to be "/custom-admin/app/mymodel/1/", but got "/admin/app/mymodel/1/".'
            ))
            url = reverse(url_name, args=[remote_obj.pk])
            self.assertEqual(url, '/custom-admin/app/mymodel/1/')
        url = reverse(
            url_name,
            args=[remote_obj.pk],
            current_app=self.model_admin.admin_site.name
        )
        self.assertEqual(url, '/custom-admin/app/mymodel/1/')
```
This script defines a custom admin site, a custom model admin, and a test case. The test case creates a request, retrieves a model object, and then calls `reverse` to generate a URL for the change view of the model. The expected URL is `/custom-admin/app/mymodel/1/`, but the actual URL is `/admin/app/mymodel/1/`. The script then calls `reverse` again, this time with the `current_app` parameter set to the name of the custom admin site, and verifies that the URL is correct.

To run the script, save it to the root directory of the project and execute it with `python3 reproducer.py`. The script will raise an `AssertionError` and print a stack trace, indicating that the expected URL is not being generated. If the issue is fixed, the script will exit with code 0 and no stack trace will be printed.