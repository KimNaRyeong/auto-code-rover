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

def main():
    try:
        from html import escape as stdlib_escape
        from django.utils.html import escape as django_escape

        test_string = "O'Reilly & Associates"
        django_escaped = django_escape(test_string)
        stdlib_escaped = stdlib_escape(test_string)

        # Check if the output of Django's escape and stdlib's escape match
        assert django_escaped == stdlib_escaped, "Output of escape functions do not match."

        # Since the issue is present when stdlib's escape outperforms Django's, we simulate a performance comparison.
        # Note: These simple time measurements are not highly accurate but suffice for demonstration purposes.
        import timeit

        django_time = timeit.timeit('escape(test_string)', setup='from django.utils.html import escape; test_string="O\'Reilly & Associates"', number=100000)
        stdlib_time = timeit.timeit('escape(test_string)', setup='from html import escape; test_string="O\'Reilly & Associates"', number=100000)

        assert stdlib_time < django_time, "stdlib escape function does not outperform Django's."

        # The concern about character encoding differences.
        assert '&#39;' in django_escaped, "Django's escape does not use '&#39;' for apostrophes."
        assert '&#x27;' in stdlib_escaped, "stdlib escape does not use '&#x27;' for apostrophes."

        print("No AssertionError raised. The issue seems to be fixed!")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
