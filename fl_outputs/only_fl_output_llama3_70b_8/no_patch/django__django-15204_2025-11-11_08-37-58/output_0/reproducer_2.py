import os
from django import forms
from django.utils.dateparse import parse_duration

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

def test_duration_field():
    class DurationFieldForm(forms.Form):
        duration = forms.DurationField()

    form = DurationFieldForm({'duration': 'P3(3D'})
    try:
        form.full_clean()
    except ValueError as e:
        print_stacktrace(e)
        assert False, "DurationField.clean fails to handle broken data"

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.conf.global_settings')
    import django
    django.setup()
    test_duration_field()
