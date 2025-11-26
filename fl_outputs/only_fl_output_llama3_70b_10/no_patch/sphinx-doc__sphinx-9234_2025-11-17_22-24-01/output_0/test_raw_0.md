Here is a Python script `reproducer.py` that reproduces the issue:
```
import requests
from urllib.parse import urlparse, urlunparse

def check_redirect(url):
    response = requests.head(url, allow_redirects=True)
    if response.status_code == 302:  # Found (redirect)
        redirect_url = response.headers['Location']
        parsed_url = urlparse(url)
        parsed_redirect_url = urlparse(redirect_url)
        if parsed_url.netloc != parsed_redirect_url.netloc:
            raise AssertionError(f"Unknown redirect from {url} to {redirect_url}")

def main():
    urls_to_check = [
        "https://www.sphinx-doc.org/",  # should be allowed
        "https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/",  # should raise AssertionError
    ]

    for url in urls_to_check:
        try:
            check_redirect(url)
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == "__main__":
    main()
```
This script uses the `requests` library to send a HEAD request to each URL and checks if it receives a 302 redirect response. If it does, it extracts the redirect URL from the `Location` header and compares the netloc (network location) parts of the original and redirect URLs. If they don't match, it raises an `AssertionError`.

The script defines two URLs to check: one that should be allowed (sphinx-doc.org) and one that should raise an error (the Windows blog URL). When run, the script will print a stack trace and exit with code 1 if the issue is present, or exit with code 0 if the issue is fixed.