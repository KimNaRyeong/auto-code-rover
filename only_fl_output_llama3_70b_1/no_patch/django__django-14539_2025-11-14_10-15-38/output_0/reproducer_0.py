import re
from urllib.parse import quote

def urlize(text):
    # This implementation is simplified to focus on the issue at hand
    pattern = r'(\b(?:(?:https?|ftp|file):\/\/|www\.)([-A-Za-z0-9+&@#/%?=~_|!:,.;]*)\b)'
    def replacer(match):
        url = match.group(0)
        return f'<a href="http://{quote(url)}">{url}</a>'
    return re.sub(pattern, replacer, text)

def main():
    input_string = 'Search for google.com/?q=1&lt! and see.'
    expected_output = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'
    actual_output = urlize(input_string)
    
    try:
        assert actual_output == expected_output
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
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
    
    main()
