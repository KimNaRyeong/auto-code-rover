import timeit
from django.utils.html import escape as django_escape
import html

def test_django_escape():
    copyright = "Copyright 2023"
    result = django_escape(copyright)
    assert result == "&copy;2023", f"Expected &copy;2023, got {result}"

def test_html_escape():
    copyright = "Copyright 2023"
    result = html.escape(copyright)
    assert result == "&#x27;Copyright 2023", f"Expected &#x27;Copyright 2023, got {result}"

def test_performance_django_escape():
    setup_code = "from django.utils.html import escape"
    stmt = "escape('Copyright 2023')"
    number = 50000
    time_taken = timeit.timeit(stmt, setup=setup_code, number=number)
    assert time_taken > 2.45, f"Expected time taken to be more than 2.45 usec, got {time_taken} usec"

def test_performance_html_escape():
    setup_code = "import html"
    stmt = "html.escape('Copyright 2023')"
    number = 100000
    time_taken = timeit.timeit(stmt, setup=setup_code, number=number)
    assert time_taken < 2.45, f"Expected time taken to be less than 2.45 usec, got {time_taken} usec"

def main():
    try:
        test_django_escape()
        test_html_escape()
        test_performance_django_escape()
        test_performance_html_escape()
        print("Issue is fixed")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
