import unicodedata
from django.utils.text import slugify

def test_slugify():
    title = "Hello İstanbul"
    slugified_title = slugify(title, allow_unicode=True)
    assert slugified_title.isalnum(), f"Slugification failed for '{title}'"

try:
    test_slugify()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
