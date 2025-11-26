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

def main():
    url = "https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/"
    expected_url = "https://blogs.windows.com/windowsdeveloper/2016/12/02/symlinks-windows-10/"
    
    try:
        check_redirect(url, expected_url)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script sends a HEAD request to the given URL and checks if the redirected URL is allowed. If not, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace. If the issue is fixed, it will exit with code 0.