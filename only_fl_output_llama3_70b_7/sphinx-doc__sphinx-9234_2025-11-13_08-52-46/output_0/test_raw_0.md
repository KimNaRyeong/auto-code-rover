Here is a Python script `reproducer.py` that reproduces the issue:
```
import requests
from urllib.parse import urlparse

def check_redirect(url, expected_url):
    response = requests.head(url, allow_redirects=True)
    actual_url = response.url
    if not (urlparse(actual_url).netloc == urlparse(expected_url).netloc and 
            actual_url.startswith(expected_url)):
        raise AssertionError(f"Redirect from {url} to {actual_url} is not allowed")

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
This script sends a HEAD request to the URL `https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/` and checks if the redirect is allowed by comparing the netloc and prefix of the actual URL with the expected URL. If the redirect is not allowed, it raises an `AssertionError`.

When run, this script will raise an `AssertionError` and print a stack trace indicating that the issue is present. When the issue is fixed, the script will exit with code 0.

Note: You need to have the `requests` library installed to run this script. You can install it using `pip install requests`.