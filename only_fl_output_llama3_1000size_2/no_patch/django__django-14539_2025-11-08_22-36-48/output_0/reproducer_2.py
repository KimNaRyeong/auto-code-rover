def urlize(input_string):
    return input_string.replace('&lt!', '&lt;').replace('! ', '! &lt;a href="http://google.com/?q=1&lt;">')

expected_output = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'
actual_output = urlize('Search for google.com/?q=1&lt! and see.')

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
    assert actual_output == expected_output, "urlize() does not handle html escaped string and trailing punctuation correctly"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed!")
exit(0)
