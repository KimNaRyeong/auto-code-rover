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

def check_url_with_headers(url, headers):
    response = requests.head(url, headers=headers)
    return response.status_code

def main():
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    headers_with_accept = {"Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"}
    headers_without_accept = {}  # Let's simulate a request without the Accept header
    
    status_with_accept = check_url_with_headers(url, headers_with_accept)
    status_without_accept = check_url_with_headers(url, headers_without_accept)
    
    try:
        # Expect a 406 response due to the Accept header issue
        assert status_with_accept == 406, "Expected 406 Not Acceptable status with Accept header"
        
        # Expecting a successful response when the Accept header is not set
        assert status_without_accept == 200, "Expected 200 OK status without Accept header"
        
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code if the issue is reproduced

if __name__ == "__main__":
    main()
    # If the script hasn't exited by this point, the issue could not be reproduced under the current conditions
    print("Issue could not be reproduced.")
    exit(0)
