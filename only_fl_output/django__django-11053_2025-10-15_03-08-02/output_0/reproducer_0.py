# reproducer.py

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
    import types
    from django.conf import settings

    try:
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        assert hasattr(settings, 'foo'), "Expected 'settings' to not have attribute 'foo'"
        assert hasattr(settings, 'baz'), "Expected 'settings' to not have attribute 'baz'"
        assert settings.foo == "bar", "Attribute 'foo' should be set to 'bar'"
        assert settings.baz == "qux", "Attribute 'baz' should be set to 'qux'"
        raise AssertionError("Non-uppercase settings were allowed and did not raise an error")
    except AssertionError as e:
        print("Issue reproduced successfully.", file=sys.stderr)
        print_stacktrace(e)
    except Exception as e:
        print("Unexpected error:", file=sys.stderr)
        print_stacktrace(e)
        exit(1)
    else:
        print("No issue detected. The script executed as expected.")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
