Here is the reproducer script:

```python
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
    from django.db import models
    from django.contrib import admin
    from django.forms.models import ModelForm
    from django.forms.widgets import HiddenInput

    class Thing(models.Model):
        pass

    class RelatedModel(models.Model):
        thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
        plop = models.CharField(max_length=42)

    class RelatedModelForm(forms.ModelForm):
        def clean(self):
            raise ValidationError("whatever")

        class Meta:
            model = RelatedModel
            fields = ('plop', )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['plop'].widget = HiddenInput(initial=['test'])

    admin.site.register(Thing)

    request = None

    form = RelatedModelForm({'plop': ['test']})
    if not form.errors:
        raise AssertionError("Expected error")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script creates a Django project and models, then attempts to create an instance of the `Thing` model with an inline form. If the error is not raised, it raises an assertion error.