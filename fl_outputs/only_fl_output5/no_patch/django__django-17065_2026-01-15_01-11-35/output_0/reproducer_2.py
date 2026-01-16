# reproducer.py

import sys
from django.core.management import execute_from_command_line

# Initialize Django environment
def setup_django_env():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_I18N=True,
        SECRET_KEY='thisisjustforreproductionpurposessoitsnotsecure',
    )
    import django
    django.setup()

# Print stack trace on exception
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

# The function to reproduce the issue
def reproduce_issue():
    from django import forms
    from django.test import SimpleTestCase

    class TestForm(forms.Form):
        data = forms.CharField(help_text="Some help text")

    class BoundFieldTests(SimpleTestCase):
        def test_as_widget_with_custom_aria_describedby(self):
            form = TestForm({"data": "some value"})
            rendered_widget = form["data"].as_widget(attrs={"aria-describedby": "custom_help_text_id"})
            expected_html = """
                <input type="text" name="data" value="some value" aria-describedby="custom_help_text_id" required id="id_data">
            """
            self.assertHTMLEqual(rendered_widget.strip(), expected_html.strip())

    try:
        test_suite = BoundFieldTests()
        test_suite.test_as_widget_with_custom_aria_describedby()
        print("The issue is not present.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    setup_django_env()
    reproduce_issue()
