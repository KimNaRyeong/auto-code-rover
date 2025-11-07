import urllib.request
import io

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
    url = "https://bpaste.net/api"
    data = b'/* some arbitrary binary data */\x00\x01\x02'
    try:
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/octet-stream')
        req.add_header('X-Selection', 'python3')  # Change to 'text' to fix the issue
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print_stacktrace(e)
        assert False, "HTTP Error 400: Bad Request"

if __name__ == "__main__":
    main()
