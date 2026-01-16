```python
# reproducer.py
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

def check_url(url: str):
    try:
        response = requests.get(url)
        # Expecting a 200 OK status, which means the request was successful.
        assert response.status_code == 200, f"Failed to retrieve {url} - Status code: {response.status_code}"
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate failure

def main():
    urls = [
        "http://bit.ly/1x5vKWM",
        "http://bit.ly/1yPgqvg",
        "http://style.shoedazzle.com/dmg/3AE3B8?dzcode=FBT&dzcontent=FBT_SDZ_CPM_Q414&pid=112768085&aid=285880402&cid=0&publisher=%25ppublisher=!;&placement=%25pplacement=!;"
    ]
    
    for url in urls:
        check_url(url)
    
    print("All URLs resolved successfully.")

if __name__ == "__main__":
    main()
```

This Python script, `reproducer.py`, attempts to retrieve the contents at the given URLs using the `requests.get` method. It raises an `AssertionError` when a request fails to retrieve content (i.e., does not return a 200 status code). It will use the provided `print_stacktrace` function to print tracebacks properly, making it easier to diagnose issues. The script exits with code 0 when all URLs are correctly fetched, indicating the absence of the issue. If an exception is caught or an assertion is triggered, it prints the stack trace and exits with code 1.