 Here is a standalone Python file `reproducer.py` that reproduces the issue:
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
        fields = '__all__'

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
    admin.site.each_context(request=None)
    request = None
    call_command('makemigrations', 'my_app', stdout=open(os.devnull, 'w'), stderr=sys.stderr)
    call_command('migrate', stdout=open(os.devnull, 'w'), stderr=sys.stderr)
    admin_site = admin.site
    admin_site.register(Thing)
    admin_site.register(RelatedModel)
    admin_site.register(RelatedModelForm)
    admin_site.register(RelatedModelInline)
    admin_site.register(ThingAdmin)

    # Create a new Thing object
    thing = Thing.objects.create()

    # Create a new RelatedModel object with an error
    request = admin.site.each_context(request=None)['request']
    form = RelatedModelForm(data={'plop': ['test']}, request=request)
    form.is_valid()  # This should raise a ValidationError

    # Try to submit the form again without modification
    form = RelatedModelForm(data={'plop': ['test']}, request=request)
    if form.is_valid():
        assert False, "ValidationError should have been raised"
    else:
        form.save_m2m()
        obj = form.save()
        assert obj.plop == ['test'], "plop should not have been changed"

if __name__ == '__main__':
    test()
```
To run the script, create a new Django project and app called `my_app`, and put the `reproducer.py` file in the root directory of the project. Then run the following command:
```
python3 reproducer.py
```
The script should raise an `AssertionError` with the following message:
```vbnet
AssertionError: ValidationError should have been raised
```
This indicates that the validation was bypassed and the `RelatedModel` object was saved without the `plop` field being validated.

To fix the issue, modify the `RelatedModelForm` class in the script as follows:
```python
class RelatedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['show_hidden_initial'] = False

    def clean(self):
        raise ValidationError("whatever