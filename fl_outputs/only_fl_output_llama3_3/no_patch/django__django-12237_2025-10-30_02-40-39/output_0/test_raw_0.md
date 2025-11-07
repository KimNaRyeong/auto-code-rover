Here is the reproducer script in Python:

```python
import unicodedata
from django.utils.text import slugify

def main():
    title = "Hello İstanbul"
    slugified_title = slugify(title, allow_unicode=True)

    assert slugified_title.isalnum(), "Slug should be alphanumeric"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
```

This script attempts to slugify the title "Hello İstanbul" using Django's `slugify` function with `allow_unicode=True`. If the resulting slug is not alphanumeric, it raises an `AssertionError`, which is caught and printed along with a stack trace.