Here is the `reproducer.py` file that reproduces the issue:
```
import requests
from urllib.parse import urlparse, urlunparse

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

def main():
    urls = [
        "http://bit.ly/1x5vKWM",
        "http://bit.ly/1yPgqvg",
        "http://style.shoedazzle.com/dmg/3AE3B8?dzcode=FBT&dzcontent=FBT_SDZ_CPM_Q414&pid=112768085&aid=285880402&cid=0&publisher=%ppublisher=!;&placement=%pplacement=!;",
    ]

    for url in urls:
        try:
            response = requests.get(url)
            assert response.status_code == 200, f"Failed to retrieve {url}"
            print(f"Successfully retrieved {url}")
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError(f"Failed to retrieve {url}") from e

if __name__ == "__main__":
    main()
```
This script sends a GET request to each of the provided URLs using the `requests` library. If any of the requests fail or do not return a 200 status code, it raises an `AssertionError` with a message indicating which URL failed and prints the stack trace of the exception using the provided `print_stacktrace` function.

You can run this script by executing `python3 reproducer.py` in the terminal. If any of the requests fail, it will raise an `AssertionError` and print the stack trace. If all requests succeed, it will exit with code 0.