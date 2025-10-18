# reproducer.py

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


def send_to_paste_bin(data: bytes, lexer: str = "python3"):
    import urllib.parse
    import urllib.request

    url = "https://bpaste.net"
    values = {'lexer': lexer, 'expiry': '1week', 'content': data.decode('utf-8')}
    data = urllib.parse.urlencode(values).encode('ascii')

    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        return response.getcode()


def main():
    # Attempt to post contents using `lexer=python3`, which is expected to fail.
    try:
        with open("data.txt", "rb") as in_fh:
            data = in_fh.read()
        status_code = send_to_paste_bin(data, lexer="python3")
        assert status_code == 400, "Expected HTTP 400 error, but got {} instead.".format(status_code)
    except Exception as e1:
        print_stacktrace(e1)

    # Attempt to post contents using `lexer=text`, which should succeed.
    try:
        status_code = send_to_paste_bin(data, lexer="text")
        assert status_code == 200, "Expected HTTP 200 OK, but got {} instead.".format(status_code)
        print("Issue is fixed.")
    except Exception as e2:
        print_stacktrace(e2)
        raise AssertionError("Issue with `lexer=text`") from e2


if __name__ == "__main__":
    main()
