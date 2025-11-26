import os
from django.conf import settings
from django.core.checks.translation import check_language_settings_consistent
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

class TranslationCheckTests(SimpleTestCase):
    def test_languages_without_bidi(self):
        with self.settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
            result = check_language_settings_consistent(None)
            if result:
                raise AssertionError("LANGUAGES_BIDI<=LANGUAGES check is still present")

if __name__ == "__main__":
    try:
        TranslationCheckTests().test_languages_without_bidi()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue is fixed")
        exit(0)
