Here is a new standalone Python file `reproducer.py` that reproduces the issue:

```python
import unicodedata
from django.utils.text import slugify

def main():
    title = "Hello İstanbul"
    try:
        slugified_title = slugify(title, allow_unicode=True)
        if not slugified_title.isalnum():
            raise AssertionError("Invalid slug")
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.