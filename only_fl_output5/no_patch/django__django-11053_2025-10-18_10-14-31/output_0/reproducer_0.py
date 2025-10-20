# reproducer.py
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
    # Reproducing the issue as described
    import types
    from django.conf import settings

    try:
        # Ensure that settings are not already configured
        if not settings.configured:
            settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")

            # Assert conditions that would throw an AssertionError if the issue exists
            assert hasattr(settings, 'foo'), 'Settings does not have attribute `foo`, but it should.'
            assert hasattr(settings, 'baz'), 'Settings does not have attribute `baz`, but it should.'
            print(f"Settings attribute check passed: foo={settings.foo}, baz={settings.baz}")

            # The issue is identified if non-uppercase settings are allowed
            raise AssertionError("Non-uppercase settings should not be allowed.")
        else:
            print("Django settings are already configured, cannot test properly.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
