import re
from urllib.parse import quote

def urlize(text):
    # This is a simplified version of the original function
    # It's enough to reproduce the issue
    pattern = r'(\b(?:(?:https?|ftp|file):\/\/|www\.)([-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]))'
    return re.sub(pattern, lambda m: f'<a href="{quote(m.group(0), safe=":/")}">{m.group(0)}</a>', text)

def main():
    input_string = 'Search for google.com/?q=1&lt! and see.'
    expected_output = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'
    
    try:
        actual_output = urlize(input_string)
        assert actual_output == expected_output, f"Expected '{expected_output}' but got '{actual_output}'"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
