Here is the reproducer script:

```python
import re
import unicodedata
from django.utils.text import slugify

def main():
    title = "Hello İstanbul"
    slugified_title = slugify(title, allow_unicode=True)
    assert slugified_title.isalnum(), "Slug should be alphanumeric"
    print_stacktrace(AssertionError())

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script will raise an `AssertionError` when the issue is present, and it will print a stack trace of the issue.