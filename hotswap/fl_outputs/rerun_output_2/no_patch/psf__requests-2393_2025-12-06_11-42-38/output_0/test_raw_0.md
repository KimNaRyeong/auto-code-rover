 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import requests

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
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
            raise

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace for each URL that fails to be retrieved due to the percent character in the URL.

For example, the output for the first URL might look like this:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 18, in main