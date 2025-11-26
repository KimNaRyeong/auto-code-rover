Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
python
import os
import sys
from django.contrib import admin
from django.db import models
from django.forms.models import ModelForm, modelformset_factory
from django.test.utils import setup_test_environment
from django.utils.translation import deactivate_all_translations

# Define models
class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = models.CharField(max_length=42, default=list)

# Define forms
class RelatedModelForm(ModelForm):
    class Meta:
        model = RelatedModel
        fields = ('plop',)

    def clean(self):
        raise ValidationError("whatever")

RelatedModelFormSet = modelformset_factory(RelatedModel, form=RelatedModelForm, extra=1)

# Define admin classes
class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel
    extra = 1

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    inlines = [RelatedModelInline]

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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    setup_test_environment()

    # Create a test client
    from django.test.client import RequestFactory
    factory = RequestFactory()

    # Create a thing instance
    thing = Thing.objects.create()

    # Create an inline formset with initial data
    formset = RelatedModelFormSet(initial=[{'plop': 'test'}])

    # Render the formset to get the HTML
    request = factory.get('/')
    request.user = reproducer.settings.AUTH_USER_MODEL()
    context = {'inline_admin_formset': formset}
    from django.template import Context, Template
    template = Template('{% load admin_static %}{% include "admin/edit_inline/stacked.html" %}')
    html = template.render(Context(context))

    # Check if the issue is present
    assert 'test' in html, "Initial value not propagated"
    print("Issue not present, test passed!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

```
This script defines the models, forms, and admin classes to reproduce the issue. It then creates a test client, renders the inline formset with initial data, and checks if the initial value is propagated correctly. If the issue is present, it raises an `AssertionError` with a stack trace of the error.