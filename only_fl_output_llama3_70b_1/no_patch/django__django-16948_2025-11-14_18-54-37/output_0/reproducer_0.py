# reproducer.py

from django.utils.html import format_html

def test_format_html():
    name = "John"
    html = format_html(f"<i>{name}</i>")  # This should raise an AssertionError
    assert False, "format_html without args or kwargs is not deprecated"

try:
    test_format_html()
except AssertionError as e:
    print_stacktrace(e)
else:
    print("Issue is fixed")
