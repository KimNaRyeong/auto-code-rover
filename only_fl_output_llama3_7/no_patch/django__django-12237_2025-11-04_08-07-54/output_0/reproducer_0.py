import unicodedata
from django.utils.text import slugify

def test_slugify():
    title = "Hello İstanbul"
    slugified_title = slugify(title, allow_unicode=True)
    assert slugified_title == "hello-istanbul"  # expected output

try:
    test_slugify()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
