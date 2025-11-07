import timeit
from django.utils.html import escape
import html

def test_django_escape():
    copyright = 'Copyright 2023'
    result = escape(copyright)
    assert result == 'Copyright 2023', f"Expected 'Copyright 2023' but got {result}"

def test_stdlib_escape():
    copyright = 'Copyright 2023'
    result = html.escape(copyright)
    assert result == 'Copyright 2023', f"Expected 'Copyright 2023' but got {result}"

def test_performance_django_escape():
    setup_code = 'from django.utils.html import escape'
    test_code = 'escape("Copyright 2023")'
    number, repeat = 50000, 5
    times = timeit.repeat(setup=setup_code, stmt=test_code, repeat=repeat, number=number)
    fastest_time = min(times) / number
    assert fastest_time > 4.03, f"Expected django escape to be slower than 4.03 usec per loop but got {fastest_time:.2f} usec per loop"

def test_performance_stdlib_escape():
    setup_code = 'import html'
    test_code = 'html.escape("Copyright 2023")'
    number, repeat = 100000, 5
    times = timeit.repeat(setup=setup_code, stmt=test_code, repeat=repeat, number=number)
    fastest_time = min(times) / number
    assert fastest_time < 2.45, f"Expected stdlib escape to be faster than 2.45 usec per loop but got {fastest_time:.2f} usec per loop"

def main():
    try:
        test_django_escape()
        test_stdlib_escape()
        test_performance_django_escape()
        test_performance_stdlib_escape()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    main()
