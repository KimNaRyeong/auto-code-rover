import urllib.request
import urllib.parse

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

def submit_to_paste_service(contents: bytes, lexer: str = 'python3'):
    data = urllib.parse.urlencode({
        'lexer': lexer,
        'code': contents.decode('utf-8'),
    }).encode()
    req = urllib.request.Request("https://bpaste.net/api", data=data, method='POST')
    # This will return the HTTP response which can be used to check the status code or any result
    return urllib.request.urlopen(req)

def main():
    try:
        # Ensure data.txt exists with some content that triggers the error
        with open("data.txt", "rb") as in_fh:
            data = in_fh.read()
        
        # Try submitting to bpaste.net with lexer=python3, expecting to trigger an HTTP 400 error
        response = submit_to_paste_service(data)
        # If response code is not 200, we expect an error
        assert response.getcode() == 200, "Expected HTTP 200 OK, indicating an issue with lexer='python3'."

    except AssertionError as assert_error:
        print("AssertionError: The test reproduced the issue as expected.")
        # If you wish to raise the AssertionError uncomment the next line
        # raise assert_error
    except urllib.error.HTTPError as http_error:
        # Catching HTTPError separately to handle expected 400 error
        if http_error.code == 400:
            print("HTTPError: Bad Request - the issue is reproduced successfully.")
        else:
            print_stacktrace(http_error)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected Exception occurred.") from e
    else:
        print("The script didn't reproduce the issue, indicating the issue might have been fixed.")

if __name__ == "__main__":
    main()
