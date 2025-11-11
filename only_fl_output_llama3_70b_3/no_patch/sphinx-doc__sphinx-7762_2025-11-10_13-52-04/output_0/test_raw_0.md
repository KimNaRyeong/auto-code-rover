Here is the `reproducer.py` file that reproduces the issue:
```
import requests
from urllib.parse import urljoin

def main():
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    user_agent = "Sphinx/2.4.3 requests/2.23.0 python/3.7.4"

    # Reproduce the issue with hardcoded Accept header
    headers = {"User-Agent": user_agent, "Accept": "*/*"}
    response = requests.head(url, headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    print("Issue not present!")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script sends a HEAD request to the specified URL with the hardcoded `Accept` header and checks if the response status code is 200 OK. If not, it raises an `AssertionError` with a message indicating that the issue is present.

When run, this script will reproduce the issue and print a stack trace of the error.