To create a script `reproducer.py` that reproduces the mentioned issue, you can follow this example. The script uses the `requests` library to simulate the scenario described in the issue. It sends a HTTP request with specific headers to the GitHub Actions badge URL and checks the response status to verify if the problem occurs (i.e., receiving a `406 Not Acceptable` response).

Please ensure you have `requests` installed in your environment or virtual environment before running this script. If not, you can install it using `pip install requests`.

Create the `reproducer.py` file with the following content:

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

def check_http_header_issue():
    headers = {
        'User-Agent': 'Sphinx/2.4.3 requests/2.23.0 python/3.7.4',
        'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'
    }
    url = 'https://github.com/cherrypy/cheroot/workflows/Test%20suite/badge.svg'
    response = requests.get(url, headers=headers)

    try:
        assert response.status_code != 406, "Received '406 Not Acceptable', the issue is present."
        print("The issue is fixed, received a successful response.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    check_http_header_issue()
```

### How to Use the Script

- Place the `reproducer.py` script in the root directory of your project.
- Ensure you have the necessary permissions to execute the script.
- Run the script using Python 3 with the command `python3 reproducer.py`.
- The script will attempt to fetch the specified URL with custom HTTP headers. If the issue is present, it will raise an `AssertionError` and print a stack trace showing where the issue occurred.
- If the problem mentioned in the issue (receiving a `406 Not Acceptable` response) no longer occurs, the script will print a message saying the issue is fixed and exit with code 0.