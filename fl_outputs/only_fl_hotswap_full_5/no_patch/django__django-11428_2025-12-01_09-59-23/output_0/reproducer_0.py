import sys
import traceback

def print_stacktrace(e):
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

class Config:
    def ready(self):
        try:
            raise MyException("foo", "bar")
        except MyException as e:
            # This line simulates the behavior of django.utils.autoreload.raise_last_exception
            # by constructing a new exception of the same type, with 1 argument (the original exception)
            raise MyException(e)

if __name__ == "__main__":
    try:
        Config().ready()
    except Exception as e:
        print_stacktrace(e)
        assert False, "AssertionError raised, issue is present"
        sys.exit(1)
