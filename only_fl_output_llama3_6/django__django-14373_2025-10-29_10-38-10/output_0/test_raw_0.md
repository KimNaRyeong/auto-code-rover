Here is the reproducer script:

```python
import datetime
from django.utils import dateformat

def test_date_format():
    for year in range(-1000, 1):
        formatted_year = dateformat.DateFormat().Y(year)
        assert len(str(formatted_year)) == 4, f"Expected a four-digit year, but got {formatted_year}"
    print("Test passed.")

try:
    test_date_format()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test succeeded.")
exit(0)
```

This script will run the `test_date_format` function which iterates over years from -1000 to 0 and checks if the formatted year using the Y specifier in Django's dateformat module is a four-digit year. If any of these assertions fail, it will print the stack trace and exit with code 1.