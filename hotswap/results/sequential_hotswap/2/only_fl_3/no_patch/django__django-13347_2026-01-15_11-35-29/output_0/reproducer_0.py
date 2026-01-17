import sys
from django.views.debug import SafeExceptionReporterFilter

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

# Dummy setting to test with a non-string key in a dictionary
test_setting = {
    1: {'login': 'cooper', 'password': 'secret'}
}

def main():
    filter = SafeExceptionReporterFilter()
    try:
        # This line attempts to cleanse the test_setting. If the issue is present,
        # it should fail due to the non-string key.
        cleansed = filter.cleanse_setting('DUMMY_SETTING', test_setting)
        
        # Asserting that the inner dictionary is cleansed
        assert cleansed[1]['password'] == '********************', "The password should have been sanitized."
        
        # If the above assertion is true, issue might be fixed. Exiting normally.
        print("Issue not present. Exiting...")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
