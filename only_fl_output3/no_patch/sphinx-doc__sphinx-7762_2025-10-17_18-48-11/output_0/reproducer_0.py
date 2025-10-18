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

def check_url_with_accept_header(url: str):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    response = requests.head(url, headers=headers)
    return response.status_code

def check_url_without_accept_header(url: str):
    headers = {'User-Agent': 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4'}
    response = requests.head(url, headers=headers)
    return response.status_code

def run_tests():
    url = "https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg"
    
    try:
        assert check_url_without_accept_header(url) == 200, "URL should be accessible without Accept header"
        
        status_code_with_header = check_url_with_accept_header(url)
        assert status_code_with_header == 406, f"Expected 406 Not Acceptable, got {status_code_with_header} with Accept header"
        print("The issue is reproduced successfully.")
    
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    run_tests()
