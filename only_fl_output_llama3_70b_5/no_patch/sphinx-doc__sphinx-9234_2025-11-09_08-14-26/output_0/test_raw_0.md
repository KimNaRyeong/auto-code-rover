Here is a Python script `reproducer.py` that reproduces the issue:
```
import requests
from urllib.parse import urlparse, urlunparse

def get_redirected_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

def check_redirect(url, expected_url):
    redirected_url = get_redirected_url(url)
    if not (urlparse(redirected_url).netloc == urlparse(expected_url).netloc and
            urlparse(redirected_url).path.startswith(urlparse(expected_url).path)):
        raise AssertionError(f"Redirect from {url} to {redirected_url} is not allowed")

try:
    # Test case 1: Good redirect (https://www.sphinx-doc.org/ -> https://www.sphinx-doc.org/en/master/)
    check_redirect("https://www.sphinx-doc.org/", "https://www.sphinx-doc.org/en/master/")
    
    # Test case 2: Bad redirect (https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/ -> https://blogs.windows.com/windowsdeveloper/)
    check_redirect("https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/", "https://blogs.windows.com/windowsdeveloper/")
    
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script uses the `requests` library to send a HEAD request to each URL and get the redirected URL. It then checks if the redirected URL is allowed by comparing the netloc (domain) and path of the original URL with the redirected URL. If the redirect is not allowed, it raises an `AssertionError`.

The `print_stacktrace` function is used to print a detailed stack trace of the error, including line numbers.

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace. If the issue is fixed, it will exit with code 0.