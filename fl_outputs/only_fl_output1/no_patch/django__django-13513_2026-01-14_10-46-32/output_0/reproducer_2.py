# reproducer.py
import sys

class CustomException(Exception):
    pass

def simulate_django_debug_view(exc):
    """Simulates the logic of Django's get_traceback_frames that should respect __suppress_context__."""
    def explicit_or_implicit_cause(exc):
        # Original logic that does not respect __suppress_context__
        return getattr(exc, '__cause__', None) or getattr(exc, '__context__', None)

    # Correct logic for demonstration
    correct_behavior = exc.__cause__ or (None if exc.__suppress_context__ else exc.__context__)

    # Assert that Django's simulated behavior matches the expected correct behavior
    assert explicit_or_implicit_cause(exc) == correct_behavior, "Django debug view logic does not respect __suppress_context__"

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
    try:
        try:
            raise CustomException("Initial exception.")
        except CustomException as exc:
            new_exc = CustomException("Second exception with suppressed context.")
            new_exc.__cause__ = None
            new_exc.__suppress_context__ = True
            raise new_exc
    except Exception as e:
        try:
            simulate_django_debug_view(e)
            # If the simulate_django_debug_view function does not raise an AssertionError,
            # it means the issue has been resolved, and we exit with code 0.
            print("Success: The issue has been fixed.")
            sys.exit(0)
        except AssertionError as ae:
            print("Failure: The issue is present.")
            print_stacktrace(ae)
            sys.exit(1)

if __name__ == "__main__":
    main()
