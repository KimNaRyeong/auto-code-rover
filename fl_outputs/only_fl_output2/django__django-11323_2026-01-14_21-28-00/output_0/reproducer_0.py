# reproducer.py

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisasecret',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    ROOT_URLCONF=__name__,
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ]
)

# Ensure Django is ready to run commands
import django
django.setup()

class FooForm(forms.Form):
    a_date = forms.DateField(widget=forms.SelectDateWidget, required=True)

def check_select_date_widget_rendering():
    form = FooForm()
    rendered_form_str = str(form)
    if 'select name="a_date_month" required id="id_a_date_month"><option value="1">' not in rendered_form_str:
        raise AssertionError("Required SelectDateWidget does not render valid HTML according to W3 standards.")

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

if __name__ == "__main__":
    try:
        check_select_date_widget_rendering()
        print("No issue detected.")
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
else:
    raise SystemExit(0)
