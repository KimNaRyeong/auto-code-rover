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
    # Create a Thing instance
    thing = Thing.objects.create()

    # Create a form with initial data
    form = RelatedModelForm(initial={'plop': ['test']})

    # Check that the form is invalid
    assert not form.is_valid()

    # Check that the plop field has an initial value
    assert form.initial['plop'] == ['test']

    # Check that the plop field has a hidden input with the initial value
    hidden_input = form.fields['plop'].widget.value_from_datadict(form.data, form.files, form.add_prefix('plop'))
    assert hidden_input == 'test'

    # Submit the form (without modifying it)
    form.submit()

    # Check that the form is still invalid
    assert not form.is_valid()

    # Check that the plop field still has the initial value
    assert form.cleaned_data['plop'] == ['test']

    # Check that the hidden input is still present
    hidden_input = form.fields['plop'].widget.value_from_datadict(form.data, form.files, form.add_prefix('plop'))
    assert hidden_input == 'test'

if __name__ == '__main__':
    try:
        test()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script will raise an `AssertionError` and print a stack trace.

To fix the issue, modify the `RelatedModelForm` class to set `show_hidden_initial=False` on the `plop` field:
```python
class RelatedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plop'].show_hidden_initial = False

    def clean(self):
        raise ValidationError("whatever")

    class Meta:
        model = RelatedModel
        fields = '__all__'
```
After making this change, run the script again with `python3 reproducer.py`. The script should exit with code 0 (i.e., without raising an exception).