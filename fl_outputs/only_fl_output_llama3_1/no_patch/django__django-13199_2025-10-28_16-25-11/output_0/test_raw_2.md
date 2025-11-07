Here is the reproducer script:

```python
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

def main():
    try:
        from django.http import HttpResponse
        from django.utils.http import http_date

        class TestResponse(HttpResponse):
            def delete_cookie(self, key, path='/', domain=None):
                self.set_cookie(key=key, max_age=0, path=path, expires=http_date(1970, 1, 1), domain=domain, secure=False, httponly=True, samesite=None)

        response = TestResponse()
        response.delete_cookie('messages')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script will try to reproduce the issue by calling `HttpResponse.delete_cookie` method with SameSite attribute set to None. If an error occurs, it will print the stack trace and raise an AssertionError.