# reproducer.py
def main():
    import types
    from django.conf import settings

    try:
        # Configuration that should not be allowed according to the documentation
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")

        # Attempt to access settings that should not have been configured
        foo = settings.foo
        baz = settings.baz

        # If both settings are successfully retrieved, the issue is present
        # This raises an AssertionError to indicate the presence of the bug
        raise AssertionError("settings.configure() allowed non-uppercase settings.")

    except AttributeError as e:
        print("The issue is fixed. Non-uppercase settings can't be accessed.")
        exit(0)  # Exit successfully indicating the issue is fixed

    except AssertionError as e:
        # If an AssertionError was raised, it means the issue is present
        # Print the stack trace to help with debugging
        print_stacktrace(e)
        exit(1)  # Exit with error code indicating the issue is still present

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
    main()
