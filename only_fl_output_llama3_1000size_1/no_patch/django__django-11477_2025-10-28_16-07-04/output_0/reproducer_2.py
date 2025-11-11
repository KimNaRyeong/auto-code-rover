import re
from urllib.parse import urlparse, urlunparse

def translate_url(pattern, path):
    parsed_path = urlparse(path)
    parts = list(parsed_path)
    match = re.fullmatch(pattern, parts[2])
    if not match:
        raise AssertionError("translate_url() creates an incorrect URL when optional named groups are missing in the URL pattern")
    return urlunparse(parts)

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

if __name__ == "__main__":
    pattern = r"(?P<optional_group>foo|bar)"
    path = "http://example.com/path/123"
    try:
        translate_url(pattern, path)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
