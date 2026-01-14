import sys
import traceback

from django.views import View


def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


class TestView(View):
    def get(self, request, *args, **kwargs):
        try:
            raise RuntimeError('my error')
        except Exception as exc:
            new_exc = ValueError('my new error')
            new_exc.__cause__ = exc
            new_exc.__suppress_context__ = True
            raise new_exc


def main():
    try:
        TestView().get(None, None)
    except ValueError as e:
        if e.__context__:
            raise AssertionError("The issue is present") from e
        print_stacktrace(e)
        sys.exit(0)


if __name__ == "__main__":
    main()
