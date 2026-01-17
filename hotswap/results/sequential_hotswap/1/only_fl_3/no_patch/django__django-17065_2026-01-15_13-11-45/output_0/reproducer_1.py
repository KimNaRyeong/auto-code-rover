# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.forms import Form, CharField
from django.test import SimpleTestCase

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

# Minimal settings required for the test
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='thisisasecretkey',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_I18N=True,
)

django.setup()

class BoundFieldTests(SimpleTestCase):
    def test_as_widget_with_custom_aria_describedby(self):
        class TestForm(Form):
            data = CharField(help_text="Some help text")
        
        form = TestForm({"data": "some value"})
        try:
            self.assertHTMLEqual(
                form["data"].as_widget(attrs={"aria-describedby": "custom_help_text_id"}),
                """
                <input type="text" name="data" value="some value"
                aria-describedby="custom_help_text_id" required id="id_data">
                """,
            )
            print("Issue is fixed.")
            exit(0)
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == "__main__":
    test_suite = BoundFieldTests()
    test_suite.test_as_widget_with_custom_aria_describedby()
