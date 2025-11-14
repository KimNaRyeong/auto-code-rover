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
    data = b'...'  # Replace with the contents of the attached data.txt file
    try:
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/octet-stream')
        urlopen = urllib.request.urlopen
        response = urlopen(req)
        assert response.getcode() == 200
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("HTTP Error occurred")

if __name__ == "__main__":
    main()
