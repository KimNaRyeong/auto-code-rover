import re
import sys

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

def slugify(value):
    """Simplified version of Django's slugify that focuses on the bug reproduction."""
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def test_bug():
    """Reproduce the 'İ' to 'i' slugify issue."""
    input_str = "İ"
    expected_slug = "i"
    slug = slugify(input_str)
    # Check both conditions that might indicate the bug
    # 1. The generated slug does not match the expected output.
    # 2. Ensuring the bug where 'İ' lowercases to 'i̇' (with dot) is caught.
    if slug != expected_slug or "̇" in slug:  # Explicitly check if 'COMBINING DOT ABOVE' is present.
        raise AssertionError(f"Slugify did not return the expected result. Got '{slug}' instead of '{expected_slug}'.")

try:
    test_bug()
    print("The issue seems to be fixed.")
    sys.exit(0)  # Exit with code 0 when the issue is fixed or not found.
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with code 1 when the issue is present, indicating failure.
