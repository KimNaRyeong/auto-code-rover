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

def test_html_escape_performance_and_output():
    try:
        # Original Django html.escape() performance and output
        from django.utils.html import escape as django_escape
        django_escape_timeit = "from django.utils.html import escape; escape('copyright')"
        django_escape_output = django_escape("'")

        # Python stdlib html.escape() performance and output
        import html
        stdlib_escape_timeit = "from html import escape; escape('copyright')"
        stdlib_escape_output = html.escape("'")

        # Measuring the performances
        import timeit

        django_time = timeit.timeit(django_escape_timeit, number=100000)
        stdlib_time = timeit.timeit(stdlib_escape_timeit, number=100000)

        # Asserting the performance improvement and output equivalence
        assert stdlib_time < django_time, "stdlib html.escape() is not faster than Django's escape."
        
        # HTML entities like '&#39;' and '&#x27;' are functionally equivalent but checking for an exact match
        assert django_escape_output == stdlib_escape_output, "The escaped outputs are not the same."
        
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exists with non-zero when assertion fails indicating an issue
    
    print("No issues found. The test has passed successfully.")
    exit(0)  # Exits with 0 indicating success/the issue has been fixed

if __name__ == "__main__":
    test_html_escape_performance_and_output()
