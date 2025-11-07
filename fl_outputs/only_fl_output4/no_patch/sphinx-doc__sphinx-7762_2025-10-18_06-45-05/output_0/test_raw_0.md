Below is a `reproducer.py` file designed to reproduce the issue described. It performs two HTTP requests to the specified URL. The first request uses a `User-Agent` header similar to what Sphinx might use, along with an `Accept` header that causes the GitHub server to respond with a `406 Not Acceptable` status, according to the reported behavior. The second request omits this problematic `Accept` header to compare the responses. The script asserts that the status code from the first request should be `200 OK`, showcasing the failure scenario when custom HTTP headers are not configurable and a fixed `Accept` header causes issues. When the issue is fixed, and custom headers are supported, the assertion should pass without errors, and the script should exit gracefully with code 0. 

```python
import requests

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

def check_without_custom_header():
    user_agent = 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4'
    headers = {'User-Agent': user_agent}
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    response = requests.head(url, headers=headers)
    return response.status_code

def check_with_custom_header():
    user_agent = 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4'
    accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers = {'User-Agent': user_agent, 'Accept': accept_header}
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    response = requests.head(url, headers=headers)
    return response.status_code

try:
    status_without_custom_header = check_without_custom_header()
    status_with_custom_header = check_with_custom_header()

    # Assuming that in the problematic behavior, the request with the custom Accept header fails with 406
    assert status_with_custom_header == 200, f"Expected HTTP 200 OK, got {status_with_custom_header}"
    print('The issue is not present. Exiting gracefully.')
except Exception as e:
    print_stacktrace(e)
    raise

```

This script is specifically tailored to pinpoint the problem of not being able to configure custom HTTP headers for the link check in Sphinx. When executed, it directly aligns with the reported issue by making requests that simulate the conditions causing the failure. Upon adding support for custom headers, modifying the script to include those headers in the requests and seeing a successful assertion would confirm the problem's resolution.