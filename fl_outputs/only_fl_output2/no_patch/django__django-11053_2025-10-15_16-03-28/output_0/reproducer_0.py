import sys

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
    import types
    from django.conf import settings

    # Attempt to configure settings using non-uppercase keys
    try:
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        # Access to potentially misconfigured settings should raise an assertion error if the issue exists
        assert hasattr(settings, 'foo') == False, "settings should not allow 'foo' because it's not uppercase"
        assert hasattr(settings, 'baz') == False, "settings should not allow 'baz' because it's not uppercase"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code when an exception occurs
    
    # If the script reaches this point without any assertions or exceptions,
    # then it's assumed that Django's settings handling has been modified to disallow non-uppercase settings as expected.
    print("Success: Non-uppercase settings are correctly disallowed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
