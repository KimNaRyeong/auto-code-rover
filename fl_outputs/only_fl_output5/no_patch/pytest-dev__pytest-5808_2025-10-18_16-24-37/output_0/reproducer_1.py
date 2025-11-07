# reproducer.py
import urllib.request
import urllib.parse
import sys
import json

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

def main():
    # Encode the data to be sent to bpaste.net, setting lexer to python3
    data = {
        'lexer': 'python3',
        'code': 'print("Hello World")',
        'expiry': '1week',
        'description': 'pytest output'
    }
    data_encoded = urllib.parse.urlencode(data).encode()

    # Construct the request
    req = urllib.request.Request(
        "https://bpaste.net",
        data=data_encoded,
        method='POST'
    )

    # Perform the HTTP request
    try:
        with urllib.request.urlopen(req) as response:
            # If the response is successful, it implies the issue might be fixed
            # But let's check the content to be sure
            content = response.read().decode('utf-8')
            # Success condition (potentially checking for expected landing URL or content snippet)
            if "Successfully" in content:
                print("Issue is fixed.")
                sys.exit(0)
            else:
                raise AssertionError("Unexpected content received, the issue may still be present.")
    except urllib.error.HTTPError as e:
        # Specifically catch the HTTPError to print a custom stack trace
        if e.code == 400:
            print_stacktrace(e)
            raise AssertionError("The issue is present: HTTP Error 400: Bad Request") from e
        else:
            print_stacktrace(e)
            raise AssertionError(f"Unexpected HTTP error: {e.code}") from e
    except Exception as e:
        # Catch other exceptions to print their traceback and re-raise them
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
