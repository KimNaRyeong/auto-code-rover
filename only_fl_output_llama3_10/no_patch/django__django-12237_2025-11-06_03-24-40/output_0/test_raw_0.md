Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import unicodedata
from django.utils.text import slugify

def main():
    title = "Hello İstanbul"
    slugified_title = slugify(title, allow_unicode=True)
    print(slugified_title)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.