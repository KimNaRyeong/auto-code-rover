import urllib.request
import re

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

def check_github_anchor(url: str, anchor: str):
    try:
        # Fetch the content of the page without the anchor
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
        
        # Attempt to find the anchor in the page content
        # This is a basic and not fully accurate simulation of anchor checking
        anchor_pattern = f'id="{anchor}"'
        if re.search(anchor_pattern, content, re.IGNORECASE) is None:
            raise AssertionError(f"Anchor '{anchor}' not found in the page content.")
        
        print(f"Anchor '{anchor}' check passed.")
    
    except urllib.error.HTTPError as e:
        print_stacktrace(e)
        raise AssertionError(f"HTTP Error for URL: {url} with code {e.code}")

def main():
    try:
        # Split URL and anchor for testing
        url = "https://github.com/openssl/openssl/blob/97cf1f6c2854a3a955fd7dd3a1f113deba00c9ef/crypto/evp/evptests.txt"
        anchor = "L232"
        check_github_anchor(url, anchor)
        print("The issue seems to be fixed. Exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
