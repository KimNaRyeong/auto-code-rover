import os
import sys
from django.utils.autoreload import raise_last_exception

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

class MyException(Exception):
    def __init__(self, value: str, other_thing: str):
        super().__init__(value)
        self.ot = other_thing

def main():
    try:
        raise_last_exception(MyException("foo", "bar"))
    except TypeError as e:
        print_stacktrace(e)
        assert False, "Expected MyException to be re-raised"
    except Exception as e:
        if not isinstance(e, MyException):
            print_stacktrace(e)
            assert False, f"Expected MyException, got {e.__class__.__name__}"
        # If we reach here, it means the issue is fixed
        sys.exit(0)

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    main()
