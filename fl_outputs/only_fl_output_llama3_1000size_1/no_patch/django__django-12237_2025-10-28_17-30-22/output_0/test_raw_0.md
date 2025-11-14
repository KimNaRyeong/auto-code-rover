Here is a standalone Python file `reproducer.py` that reproduces the issue:

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

You can run this script by executing `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace.