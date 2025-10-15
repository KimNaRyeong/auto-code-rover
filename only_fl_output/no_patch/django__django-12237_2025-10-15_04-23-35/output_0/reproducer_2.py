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

try:
    import re
    import unicodedata
    from django.utils.text import slugify
    
    # Simulate Django's original slugify unicode regex pattern
    slug_unicode_re = re.compile(r'^[-\w]+\Z', re.U)

    title = "Hello İstanbul"
    expected_slug = "hello-istanbul"
    slug_result = slugify(title, allow_unicode=True)

    # Check all characters in slugified result against the regex
    for character in slug_result:
        if not slug_unicode_re.match(character):
            unicoded_name = unicodedata.name(character)
            raise AssertionError(f"Character '{character}' ({unicoded_name}) is not a valid slug character.")

    assert slug_result == expected_slug, f"Slugify returned unexpected result: {slug_result}. Expected: {expected_slug}"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Signal failure with non-zero exit code
except Exception as e:
    print_stacktrace(e)
    exit(1)  # General error catch-all with non-zero exit code
else:
    print("SUCCESS: The slug was generated correctly.")
    exit(0)  # Success exit code
