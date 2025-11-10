import os
import sys
from django.core.checks import Error
from django.utils.translation import get_language_info

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
    try:
        LANGUAGES = [('en', 'English')]
        LANGUAGES_BIDI = [('ar', 'Arabic'), ('fa', 'Persian')]

        if not set(LANGUAGES).issubset(set(LANGUAGES_BIDI)):
            raise AssertionError("LANGUAGES_BIDI is not a subset of LANGUAGES")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
