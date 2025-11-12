Here is a Python script `reproducer.py` that reproduces the issue:
```
import requests
from urllib.parse import urlparse, urlunparse

def get_redirected_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

def main():
    original_url = "https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/"
    expected_url = "https://blogs.windows.com/windowsdeveloper/2016/12/02/symlinks-windows-10/"

    redirected_url = get_redirected_url(original_url)

    # This should raise an AssertionError if the issue is present
    assert urlparse(redirected_url) == urlparse(expected_url), f"Redirected URL {redirected_url} does not match expected URL {expected_url}"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script sends a HEAD request to the original URL, which redirects to a new URL. It then checks if the redirected URL matches the expected URL. If they don't match, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.