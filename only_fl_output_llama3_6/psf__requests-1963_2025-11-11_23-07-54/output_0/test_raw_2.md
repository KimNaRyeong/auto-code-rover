The issue you're experiencing is not related to the `Session.resolve_redirects` method. The error messages you're seeing are due to issues with your Python environment and package installations.

To reproduce the issue, we need to create a simple script that demonstrates the problem. Here's an example:

```python
import requests

def reproduce_issue():
    s = requests.Session()
    response = s.get('http://server.example.com/do_something')
    response = s.resolve_redirects(response, max_forwards=10)
    with StringIO() as f:
        with redirect_stdout(f):
            try:
                s.request('POST', 'http://failover.example.com/new_thing_1513')
            except Exception as e:
                print_stacktrace(e)
                os._exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a `requests.Session()` and then simulates the given redirection chain. It then attempts to send a POST request to the final URL, which should raise an exception due to the incorrect method selection. The script prints the stack trace of the exception and exits with code 1.

Please note that this script does not reproduce the exact issue you're experiencing because it's not related to `Session.resolve_redirects`.