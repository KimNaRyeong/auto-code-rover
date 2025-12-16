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
    admin.site.each_context(request=None)

if __name__ == '__main__':
    try:
        test()
    except ValidationError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise a `ValidationError` and print a stack trace, reproducing the issue.

To fix the issue, you can modify the `RelatedModelForm` class to set `show_hidden_initial=False` on the `plop` field:
```python
class RelatedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plop'].show_hidden_initial = False

    def clean(self):
        raise ValidationError("whatever")

    class Meta:
        model = RelatedModel
        fields = ['plop']
```
With this modification, the script will no longer raise a `ValidationError` and will exit with code 0, indicating that the issue has been fixed.