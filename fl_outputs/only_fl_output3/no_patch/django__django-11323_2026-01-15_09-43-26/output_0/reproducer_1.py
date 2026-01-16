# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

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

# Setup Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=(
        # List necessary apps here
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Your test code starts here
from django import forms

class FooForm(forms.Form):
    a_date = forms.DateField(widget=forms.SelectDateWidget)

def check_select_date_widget_placeholder():
    form = FooForm()
    html_output = str(form)
    if 'required id="id_a_date_month"><option value=""' not in html_output:
        raise AssertionError("SelectDateWidget does not include an empty value option as placeholder.")
    else:
        print("The issue is fixed.")

try:
    check_select_date_widget_placeholder()
except Exception as e:
    print_stacktrace(e)
    exit(1)  # Ensure the script exits with code 1 when an Exception is raised
else:
    exit(0)  # Exit with code 0 when the issue is fixed or not present
