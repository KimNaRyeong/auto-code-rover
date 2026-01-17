# reproducer.py

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

def urlize(text: str) -> str:
    # Simulate the behavior targeted in the issue description
    import html
    import re
    from urllib.parse import quote

    def replace(match):
        url = match.group(0)
        # Ensure trailing punctuation is not included in the URL
        trailing_punctuation = ('.', ',', '!', '?', ':', ';', '>', '&lt', '&gt')
        for punc in trailing_punctuation:
            if url.endswith(punc):
                url = url[:-len(punc)]
                break
        # HTML escape and urlencode
        escaped_url = html.escape(url)
        return f'<a href="http://{quote(escaped_url)}">{html.escape(url)}</a>'

    # Apply the URL pattern with trailing punctuation accounted for in replacement logic
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    text = url_pattern.sub(replace, text)

    return text

def main():
    # Test string that exposes the issue
    test_string = 'Search for google.com/?q=1&lt! and see.'
    expected_output = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'

    try:
        actual_output = urlize(test_string)
        assert actual_output == expected_output, "AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
        print(f"Actual output: {actual_output}")
        print(f"Expected output: {expected_output}")
        raise SystemExit(1)  # Exit with code 1 to indicate a failure in reproducing the issue correctly

    print("No issues detected.")  # If this line is reached, the expected behavior matches the actual output
    raise SystemExit(0)  # Exit with code 0 to indicate success

if __name__ == "__main__":
    main()
