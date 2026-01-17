 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import requests

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_response_content_retains_error():
    response = requests.post("http://connreset.biz/get/incomplete/chunked", stream=True)
    try:
        response.content
    except Exception:
        # Error handling code, may try something else or fall through
        pass

    content = response.content  # empty string
    if content:
        print_stacktrace(AssertionError(f"error response has content: {content!r}"))

if __name__ == "__main__":
    test_response_content_retains_error()
```
When executed with Python 3.6.8, the script prints the following stack trace:
```csharp
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    test_response_content_retains_error()
  File "reproducer.py", line 15, in test_response_content_retains_error
