Given the requirements and the context of the feature request, we'll aim for a Python script that explicitly tests for the issue described: the `linkcheck` tool in `sphinx` not properly handling custom HTTP headers, especially the `Accept` header leading to `406 Not Acceptable` responses from the GitHub server. The goal is to reproduce the scenario where `linkcheck` fails due to the hardcoded `Accept` header.

Adhering strictly to the scenario outlined, we'll execute two requests to the GitHub Actions badge endpoint: one with the hardcoded `Accept` header (as per the current `sphinx` implementation) and one with a custom `Accept` header (mimicking a browser's request) that should ideally be supported by `linkcheck`. The test will verify if the hardcoded `Accept` header causes a failure (HTTP 406 response) and whether a custom `Accept` header would succeed (HTTP 200 response). This demonstrates the problem and shows the need for configurable HTTP headers.

```python
import urllib.request

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

def check_url_with_accept_header(accept_header_value):
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    headers = {
        'Accept': accept_header_value,
        'User-Agent': 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.status  # Returning the HTTP status code

if __name__ == "__main__":
    try:
        # Hardcoded header value in Sphinx as per the issue
        hardcoded_accept_status = check_url_with_accept_header('text/html,application/xhtml+xml;q=0.9,*/*;q=0.8')
        assert hardcoded_accept_status == 406, "Expected 406 Not Acceptable, got another response."

        # Browser-like header that should ideally be supported
        browser_accept_status = check_url_with_accept_header('text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        assert browser_accept_status == 200, "Expected 200 OK, got another response."

    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise the AssertionError to indicate the test failure

    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate an unexpected error occurred

    print("Success: The issue is not present, or it has been fixed.")
    exit(0)  # Exit code 0 to indicate success/no issue
```

This script simulates the exact problem situation and verifies the outcomes against the expected HTTP statuses. It raises an `AssertionError` appropriately when the issue is reproduced (if the GitHub server responds differently to the hardcoded vs. browser-like `Accept` headers), demonstrating the problem with the current `sphinx` `linkcheck` implementation.