import urllib.request
from html.parser import HTMLParser
import sys

class AnchorChecker(HTMLParser):
    def __init__(self, target_anchor):
        super().__init__()
        self.target_anchor = target_anchor
        self.found = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            if "id" in attrs_dict and attrs_dict["id"] == self.target_anchor:
                self.found = True

def check_anchor(url, anchor):
    request = urllib.request.urlopen(url)
    content = request.read().decode('utf-8')

    parser = AnchorChecker(anchor)
    parser.feed(content)
    if not parser.found:
        raise AssertionError(f"Anchor '{anchor}' not found in the document at {url}")

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

if __name__ == '__main__':
    try:
        # Replace these URLs with the appropriate GitHub pages URLs and anchors
        check_anchor("https://github.com/crate/crate-docs-theme/blob/master/DEVELOP.rst", "user-content-make-changes")
        print("Issue not present, anchor found successfully.")
        
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        sys.exit(1)
