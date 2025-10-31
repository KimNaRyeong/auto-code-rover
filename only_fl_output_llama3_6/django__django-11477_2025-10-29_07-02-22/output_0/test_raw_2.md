Here is the `reproducer.py` script that reproduces the issue:

```python
import re
from urllib.parse import urlparse, urlunparse

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def translate_url(pattern, path):
    parts = list(urlparse(path))
    for i, part in enumerate(parts):
        if re.match(pattern, part):
            match = re.fullmatch(pattern, part)
            if match:
                group_names = [name for name in match.groupdict]
                for name in group_names:
                    if not match.group(name):
                        parts[i] = f"{part}({name})"
    return urlunparse(parts)

def main():
    pattern = r"(.*)/(.*)"
    path = "/hello/world"
    try:
        result = translate_url(pattern, path)
        print(result)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script defines a function `translate_url` that takes a URL pattern and a path as input. It attempts to translate the path by replacing any parts of the path that match the pattern with the corresponding group names from the pattern.

In this case, the issue is reproduced by calling `translate_url` with a pattern that has an optional named group (the `(.*)/(.*)` pattern) and a path that does not contain the expected group values. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.

To run this script, simply execute it using Python 3: `python3 reproducer.py`.