Here is the `reproducer.py` file that reproduces the issue:
```
import django
from django import forms
from django.utils.dateparse import parse_duration

def test_duration_field():
    class MyForm(forms.Form):
        duration = forms.DurationField()

    form = MyForm({'duration': 'P3(3D'})
    try:
        form.full_clean()
    except ValueError as e:
        print_stacktrace(e)
        assert False, "DurationField.clean fails to handle broken data"

if __name__ == "__main__":
    test_duration_field()
```
<|start_header_id|>