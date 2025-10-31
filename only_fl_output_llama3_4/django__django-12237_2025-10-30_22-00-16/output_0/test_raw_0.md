Here is the reproducer script:

```python
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
```

This script defines a function `test_slugify` that calls the `slugify` function with the given title and checks if the resulting slug is alphanumeric. If the slugification fails, it raises an `AssertionError`. The script then catches this exception and prints the stack trace using the provided `print_stacktrace` function.