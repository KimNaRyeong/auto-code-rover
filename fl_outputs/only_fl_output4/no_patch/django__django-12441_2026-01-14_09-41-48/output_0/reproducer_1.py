# reproducer.py
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

# Minimal Django settings required for forms to work
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
    ),
    SITE_ID=1,
    SECRET_KEY='super-secret',
)

execute_from_command_line(['django-admin', 'migrate'])

from django import forms


class TestForm(forms.Form):
    hidden_input = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        self.add_error(None, 'Form error')
        self.add_error('hidden_input', 'Hidden input error')


def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def main():
    test_form = TestForm(data={})
    try:
        # Initially calling as_table to populate errors
        test_form.as_table()
        initial_non_field_errors_count = len(test_form.non_field_errors())
        # Another call to as_table, which should ideally not affect the errors
        test_form.as_table()
        second_non_field_errors_count = len(test_form.non_field_errors())

        # Assertion to confirm the issue
        assert initial_non_field_errors_count == second_non_field_errors_count, \
            "Multiple calls to form output methods should not increase the count of non-field errors."

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate the presence of the issue

    print("Issue not present, exiting with code 0.")
    sys.exit(0)


if __name__ == '__main__':
    main()
