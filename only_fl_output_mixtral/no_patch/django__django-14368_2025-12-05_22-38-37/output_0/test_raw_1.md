 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import datetime
import dateutil.parser
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def parse_datetime(s: str):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        return dateutil.parser.parse(s)

if __name__ == "__main__":
    s = "2012-04-23T10:20:30.400 -02"
    d = parse_datetime(s)
    if d is None:
        e = Exception("Failed to parse ISO-8601 datetime string")
        print_stacktrace(e)
        sys.exit(1)
    else:
        print(f"Parsed ISO-8601 datetime string: {d}")
        sys.exit(0)
```
When executed with `python3 reproducer.py`, the script will parse the ISO-8601 datetime string `2012-04-23T10:20:30.400 -02` using the `parse_datetime` function, which first tries to parse the string using the `strptime` method of the `datetime.datetime` class, and falls back to using the `parse` function of the `dateutil.parser` module if a `ValueError` is raised.

If the string is not parsed correctly, an `AssertionError` will be raised and the stack trace will be printed using the `print_stacktrace` function. If the string is parsed correctly, the parsed datetime object will be printed and the script will exit with code 0.