import types
import sys
import traceback

def print_stacktrace(e: Exception):
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
        class UserSettingsHolder:
            def __getattr__(self, key):
                return getattr(settings, key)

        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        print(settings.foo, settings.baz)
        assert False, "The issue was not reproduced."
    except AssertionError:
        raise
    except Exception as e:
        print_stacktrace(e)
        assert False, "An unexpected error occurred."

if __name__ == "__main__":
    reproduce_issue()
