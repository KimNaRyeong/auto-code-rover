Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import requests
import sys

def print_stacktrace(e: Exception):
    import traceback
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
    headers = {
        'User-Agent': 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4',
        'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'
    }
    try:
        response = requests.head(url, headers=headers)
        if response.status_code == 406:
            raise AssertionError("Issue present")
        else:
            print("Issue fixed")
            sys.exit(0)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script sends a HEAD request to the specified URL with custom HTTP headers and checks if the response status code is 406. If it is, an `AssertionError` is raised, indicating that the issue is present. Otherwise, it prints "Issue fixed" and exits with code 0.

To run this script, save it in a file named `reproducer.py`, then execute it using Python: `python3 reproducer.py`.