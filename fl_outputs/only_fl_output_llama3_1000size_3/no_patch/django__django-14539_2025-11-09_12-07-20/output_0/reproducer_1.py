def urlize(input_string):
    import urllib.parse
    from html.parser import HTMLParser

    class URLizer(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = []

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                href = [attr for attr in attrs if attr[0] == 'href'][0][1]
                self.result.append(f'<a href="{urllib.parse.quote(href)}">')
            else:
                self.result.append(tag)

        def handle_endtag(self, tag):
            self.result.append('</' + tag + '>')

    urlizer = URLizer()
    urlizer.feed(input_string)
    return ''.join(urlizer.result)

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
    urlized_string = urlize('Search for google.com/?q=1&lt! and see.')
    if urlized_string != 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.':
        raise AssertionError("urlize() does not handle html escaped string and trailing punctuation correctly")
except Exception as e:
    print_stacktrace(e)
    exit(1)
