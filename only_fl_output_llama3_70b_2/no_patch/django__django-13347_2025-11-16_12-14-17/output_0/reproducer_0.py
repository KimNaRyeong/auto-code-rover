import django
from django.views.debug import SafeExceptionReporterFilter

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

def test_safe_exception_reporter_filter():
    SOME_SETTING = {1: {'login': 'cooper', 'password': 'secret'}}
    filter = SafeExceptionReporterFilter()
    try:
        cleaned_setting = filter.cleanse_setting('SOME_SETTING', SOME_SETTING)
        assert isinstance(cleaned_setting, dict) and '...' in str(cleaned_setting[1]['password'])
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_safe_exception_reporter_filter()
