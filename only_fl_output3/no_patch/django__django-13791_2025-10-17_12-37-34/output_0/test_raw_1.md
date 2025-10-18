Below is the `reproducer.py` file that should replicate the issue as described. The script checks whether the `parse_duration` function from Django behaves incorrectly for cases where the timedelta only has days and especially with negative days. If the issue is present, it will raise an `AssertionError` and print a readable stack trace. The script will exit safely with code 0 if the issue does not occur (indicating a potential fix).

```python
import sys
from datetime import timedelta
from django.utils.dateparse import parse_duration

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def duration_iso_string(td: timedelta) -> str:
    # This part converts a timedelta object into its ISO 8601 formatted string including the sign.
    # It's a simplified version, real-world usage might need more complex handling.
    sign = "-" if td.total_seconds() < 0 else ""
    days, remainder = divmod(abs(td.total_seconds()), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{sign}P{int(days)}DT{int(hours)}H{int(minutes)}M{seconds}S"

def test_parse_duration_with_negative_days():
    try:
        td = timedelta(days=-1)
        iso_str = duration_iso_string(td)
        result_td = parse_duration(iso_str)
        assert result_td == td, "Failed to parse ISO string with negative days correctly."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code if the issue is present.
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code if unexpected issue occurs.

if __name__ == "__main__":
    test_parse_duration_with_negative_days()
    print("No issues detected.")
    sys.exit(0)
```

To run this script, ensure you have Django installed in your environment. This can be done via pip if not already installed:

```sh
pip install Django
```

Then, execute the script with Python 3:

```sh
python3 reproducer.py
```

If there's an issue as described, the script should output an `AssertionError` with a stack trace. If the issue has been fixed, or your Django version behaves as expected, it will print "No issues detected" and exit with code 0.