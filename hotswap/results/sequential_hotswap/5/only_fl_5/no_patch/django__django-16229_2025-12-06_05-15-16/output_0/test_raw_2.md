 I apologize for the mistake in my previous response. Here is the corrected `reproducer.py` file that reproduces the issue:
```python
import sys
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.contrib import admin
from django.db.models.fields import ArrayField

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = ArrayField(
        models.CharField(max_length=42),
        default=list,
    )

class RelatedModelForm(ModelForm):
    def clean(self):
        raise ValidationError("whatever")

    class Meta:
        model = RelatedModel
        fields = ['plop']

class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel
    extra = 1

class ThingAdmin(admin.ModelAdmin):
    inlines = [
        RelatedModelInline
    ]

admin.site.register(Thing, ThingAdmin)

def test():
    from django.test.client import Client
    from django.urls import path, include
    from django.http import HttpResponse

    admin_site = admin.site._registry

    def serve(request, *args, **kwargs):
        if request.path == '/admin/':
            request.path = '/admin/my_app/thing/add/'
        return admin_site[request.path]().admin_site.admin_view(request)

    urlpatterns = [
        path('admin/', serve),
        path('admin/', include(admin_site.urls)),
    ]

    c = Client()
    response = c.post('/admin/', {
        'thing_set-0-name': '',
        'initial-relatedmodel_set-0-plop': 'test',
        'relatedmodel_set-0-plop': '',
        'relatedmodel_set-0-thing': '1',
        'relatedmodel_set-0-id': '',
    })
    if 'whatever' not in response.content.decode():
        print("AssertionError: validation error message not found in response content")
        print_stacktrace(Exception("Validation error message not found in response content"))
        sys.exit(1)

    response = c.post('/admin/', {
        'thing_set-0-name': '',
        'relatedmodel_set-0-plop': '',
        'relatedmodel_set-0-thing': '1',
        'relatedmodel_set-0-id': '',
    })
    if 'whatever' in response.content.decode():
        print("AssertionError: validation error message still present in response content")
        print_stacktrace(Exception("Validation error message still present in response content"))
        sys.exit(1)

if __name__ == '__main__':
    test()
```
The script uses Django's test client to simulate the behavior of creating an object via the admin interface. The script asserts that the validation error message is present in the response content after the first submit, and that it is not present in the response content after the second submit.

To run the script, make sure you have Django installed and the project's settings file is in the same directory as the script. Then run the following command:
```
python3 reproducer.py
```
If the script runs successfully, it will exit with code 0. If the issue is present, it will raise an `AssertionError` and print a stack trace.