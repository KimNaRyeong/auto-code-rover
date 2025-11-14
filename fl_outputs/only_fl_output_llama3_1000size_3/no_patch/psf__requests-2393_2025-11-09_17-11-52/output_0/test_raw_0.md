Here is the reproducer script:

```python
import requests
from urllib.parse import urlparse, unquote
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    urls = [
        "http://bit.ly/1x5vKWM",
        "http://bit.ly/1yPgqvg",
        "http://style.shoedazzle.com/dmg/3AE3B8?dzcode=FBT&dzcontent=FBT_SDZ_CPM_Q414&pid=112768085&aid=285880402&cid=0&publisher=%ppublisher=!;&placement=%pplacement=!;",
    ]

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to fetch each URL using `requests.get()`. If any of the URLs fail to fetch, it will catch the exception and call `print_stacktrace()` to print the stack trace. If an assertion error is raised, it means the issue was reproduced successfully.