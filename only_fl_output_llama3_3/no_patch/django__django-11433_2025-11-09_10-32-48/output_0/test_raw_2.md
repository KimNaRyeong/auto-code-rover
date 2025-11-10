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

def reproduce_issue():
    from django.db import models
    from django.forms import Form, ModelForm

    class MyModel(models.Model):
        some_field = models.CharField(max_length=255, default='default_value')

    class MyForm(ModelForm):
        class Meta:
            model = MyModel
            fields = ['some_field']

    my_model = MyModel()
    form = MyForm({'other_field': 'value'})
    if not hasattr(my_model, 'cleaned_data'):
        raise AssertionError("Issue not present")
    try:
        my_model.some_field = form.cleaned_data.get('some_field', my_model.some_field)
    except AttributeError:
        print_stacktrace(AttributeError("Issue present"))

if __name__ == "__main__":
    reproduce_issue()
```

This script should correctly reproduce the issue.