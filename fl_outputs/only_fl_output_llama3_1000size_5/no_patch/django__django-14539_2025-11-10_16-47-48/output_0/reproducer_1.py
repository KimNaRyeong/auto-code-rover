from urllib.parse import unquote, urljoin, urlparse, quote

def urlize(input_string):
    output = ""
    for char in input_string:
        if char == '<':
            output += '&lt;'
        elif char == '>':
            output += '&gt;'
        else:
            output += char
    return output

def reproduce_issue():
    try:
        result = urlize('Search for google.com/?q=1&lt! and see.')
        expected_result = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'
        if result != expected_result:
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
    reproduce_issue()
