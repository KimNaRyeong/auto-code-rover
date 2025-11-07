Here is the reproducer script:

```python
import django
from django.utils import dateformat

def test_date_format():
    year = 500
    formatted_year = dateformat.DateFormat.Y().format(year)
    assert len(formatted_year) == 4, f"Expected a four-digit year, got {formatted_year}"
    print_stacktrace(AssertionError(f"Year {year} is not zero-padded"))

try:
    test_date_format()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Test passed")
    exit(0)
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.