Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib import admin
from django.forms.models import ModelForm
from django.forms.fields import CharField
from django.forms.widgets import TextInput
from django.forms.util import ValidationError

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

class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = models.CharField(max_length=42)
    class Meta:
        default_manager_name='objects'

class RelatedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        raise ValidationError("whatever")

class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel
    extra = 1

admin.site.register(Thing, ThingAdmin=type('ThingAdmin', (admin.ModelAdmin,), {'inlines': [RelatedModelInline]}))

def main():
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
        import django
        django.setup()
        from django.contrib.auth.models import User
        user = User.objects.create_user('testuser', 'testemail@example.com', 'testpassword')
        admin.site.register(Thing)
        form = RelatedModelForm({'plop': ['test1', 'test2']})
        if not form.is_valid():
            raise AssertionError("Expected the form to be invalid")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script sets up a Django project, creates an admin site and a model with an inline form. It then tries to create an instance of the model using the inline form and checks if the form is valid. If the form is not valid (which it should be due to the `clean` method in the form), an AssertionError is raised.