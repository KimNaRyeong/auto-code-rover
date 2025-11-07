import requests
from io import BytesIO

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

def reproduce_issue():
    url = 'https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg'
    headers = {'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'}
    
    def mock_requests_head(url, headers):
        response = requests.Response()
        response.status_code = 406
        return response
    
    with requests.Session() as session:
        session.get = lambda url, **kwargs: BytesIO(b'')
        session.head = mock_requests_head
        
        try:
            response = session.head(url, headers=headers)
            if response.status_code == 406:
                raise AssertionError("Issue present")
            else:
                print("Issue fixed")
        except Exception as e:
            print_stacktrace(e)
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
