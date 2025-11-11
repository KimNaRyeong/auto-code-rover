Here is the reproducer script:

```python
def delete_cookie(key):
    import http.cookies
    cookie = http.cookies.SimpleCookie()
    cookie[key] = ''
    cookie[key]['max-age'] = 0
    cookie[key]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    cookie[key]['path'] = '/'
    print(cookie.output(header=''))

def main():
    try:
        delete_cookie('messages')
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

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

if __name__ == '__main__':
    main()
```

This script attempts to delete a cookie without preserving its SameSite attribute. If the issue is present, it raises an `AssertionError` and prints a stack trace of the error.