Here is the reproducer script:

```python
import datetime
from django.utils import dateformat

def test_date_format():
    for year in range(-1000, 1):
        formatted_year = dateformat.format(datetime.date(year, 1, 1), 'Y')
        assert len(formatted_year) == 4, f"Expected a four-digit year, but got {formatted_year}"
        if year < 0:
            assert formatted_year.startswith('0'), f"Expected zero-padding for years less than 1000, but got {formatted_year}"

try:
    test_date_format()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script will run a series of tests to check that the `Y` format specifier in Django's date formatting module returns four-digit years, with zero-padding for years less than 1000. If any of these assertions fail, it will print the stack trace and exit with code 1.