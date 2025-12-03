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
            # re-raise the exception with custom signature
            raise MyException("re-raised", e.ot)

def main():
    try:
        Config().ready()
    except MyException as e:
        print_stacktrace(e)
        assert False, "MyException was not raised as expected"

if __name__ == "__main__":
    main()
