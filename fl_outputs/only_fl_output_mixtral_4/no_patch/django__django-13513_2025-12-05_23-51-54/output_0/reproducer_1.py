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
            exc.__suppress_context__ = True
            raise ValueError('my new error') from None


def main():
    try:
        view = TestView()
        response = view.get(None, None, None)
    except ValueError as e:
        assert e.__context__ is None, "Context should be None"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
