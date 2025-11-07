Here is the reproducer script:

```python
import unicodedata
from django.utils.text import slugify

def main():
    title = "Hello İstanbul"
    try:
        slugified_title = slugify(title, allow_unicode=True)
        print(slugified_title)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected ValidationError")

if __name__ == "__main__":
    main()
```

This script attempts to slugify the title "Hello İstanbul" with `allow_unicode=True`. If an exception is raised, it prints the stack trace and raises an `AssertionError`.