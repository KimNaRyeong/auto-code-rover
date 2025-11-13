import timeit
from django.utils.html import escape
import html

def test_django_escape():
    copyright = "Copyright 2023"
    result = escape(copyright)
    assert result == "Copyright 2023", f"Expected 'Copyright 2023', got {result}"

def test_stdlib_escape():
    copyright = "Copyright 2023"
    result = html.escape(copyright)
    assert result == "Copyright 2023", f"Expected 'Copyright 2023', got {result}"

def test_performance_django_escape():
    setup_code = "from django.utils.html import escape"
    test_code = "escape('Copyright 2023')"
    number, time_taken = timeit.Timer(test_code, setup=setup_code).autorange()
    assert time_taken > 4.03, f"Expected time taken to be more than 4.03 usec, got {time_taken} usec"

def test_performance_stdlib_escape():
    setup_code = "import html"
    test_code = "html.escape('Copyright 2023')"
    number, time_taken = timeit.Timer(test_code, setup=setup_code).autorange()
    assert time_taken < 2.45, f"Expected time taken to be less than 2.45 usec, got {time_taken} usec"

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

try:
    test_django_escape()
    test_stdlib_escape()
    test_performance_django_escape()
    test_performance_stdlib_escape()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
