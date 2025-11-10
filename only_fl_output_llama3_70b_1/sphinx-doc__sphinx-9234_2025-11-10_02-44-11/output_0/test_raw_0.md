Here is a Python script `reproducer.py` that reproduces the issue:
```python
import requests
from urllib.parse import urlparse,<|begin_of_text|>2016/12/02/symlinks-windows-10/

def check_redirect(url):
    response = requests.head(url, allow_redirects=True)
    if response.status_code == 301 or response.status_code == 302:
        redirect_url = response.headers['Location']
        parsed_url = urlparse(redirect_url)
        if parsed_url.netloc != urlparse(url).netloc:
            raise AssertionError(f"Unknown redirect from {url} to {redirect_url}")

def main():
    url = "https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/"
    try:
        check_redirect(url)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script sends a HEAD request to the problematic URL and checks if it redirects to an unknown location. If it does, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

When run with `python3 reproducer.py`, this script should raise an `AssertionError` and print a stack trace indicating the issue. When the issue is fixed, the script should exit with code 0.