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
    data = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\xed\xbd\x7f\x76\x5e\x02\x00\x21\x03\x49\x48\x44\x52\x05\x00\x03\x49\x4c\x45\x04\x00\x15\x03\x49\x4c\x45\x1b\x03\x49\x4c\x45\x12\x03\x49\x4c\x45\x0f\x03\x49\x4c\x45\x16\x03\x49\x4c\x45\x10\x03\x49\x4c\x45\x13\x03\x49\x4c\x45\x11\x03\x49\x4c\x45\x14\x03\x49\x4c\x45\x17\x00\x00\x00'
    url = "https://bpaste.net/api"
    params = {
        'lexer': 'python3',
        'format': 'text'
    }
    try:
        req = urllib.request.Request(url, data=data)
        for key, value in params.items():
            req.add_header(f'X-{key.capitalize()}', value)
        urlopen = urllib.request.urlopen(req)
        response = urlopen.read().decode('utf-8')
        print(response)
    except Exception as e:
        print_stacktrace(e)
        assert False, "HTTP Error 400: Bad Request"

if __name__ == "__main__":
    main()
